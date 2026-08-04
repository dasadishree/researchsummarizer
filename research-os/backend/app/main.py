from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from app.services.pdf_service import extract_text_from_pdf
from app.services.ai_service import create_research_card, client
from app.database.database import engine, Base, SessionLocal
from app.models import ResearchCard
import json
from collections import defaultdict

@app.get("/graph")
def get_graph_data():
    db=SessionLocal()
    papers=db.query(ResearchCard).all()
    db.close()
    nodes=[]
    edges=[]
    def parse_keywords(kw_str):
        if not kw_str:
            return []
        cleaned = kw_str.replace("[", "").replace("]", "").replace("'", "").replace("'", "")
        return [k.strip().lower() for k in cleaned.split(",") if k.strip()]
    for paper in papers:
        nodes.append({
            "id": str(paper.id),
            "label": paper.title,
            "doi": paper.doi
        })
    paper_keywords = {paper.id: parse_keywords(paper.keywords) for paper in papers}
    for i in range(len(papers)):
        for j in range(i+1, len(papers)):
            p1_id=papers[i].id
            p2_id=papers[j].id
            k1=set(paper_keywords[p1_id])
            k2=set(paper_keywords[p2_id])
            shared=k1.intersection(k2)
            if shared:
                edges.append({
                    "source": str(p1_id),
                    "target": str(p2_id),
                    "weight": len(shared),
                    "shared_keywords": list(shared)
                })
    return {"nodes": nodes, "links": edges}

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    question: str

@app.get("/")
def root():
    return{"message": "ResearchOS API is running!"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    pdf = extract_text_from_pdf(contents)
    print("extracted", pdf["word_count"], "words")
    research_card = create_research_card(pdf["text"])
    print(research_card)

    db = SessionLocal()
    existing=None

    if research_card["doi"]:
        existing = db.query(ResearchCard).filter(
            ResearchCard.doi == research_card["doi"]
        ).first()

    if existing:
        db.close()
        return {
            "message": "Paper already uploaded.",
            "paper_id": existing.id,
            "research_card": research_card
        }

    paper = ResearchCard(
        title=research_card["title"],
        doi=research_card["doi"],
        summary=research_card["summary"],
        objective=research_card["objective"],
        hypothesis=research_card["hypothesis"],
        methods=str(research_card["methods"]),
        dataset=research_card["dataset"],
        research_gap=research_card["research_gap"],
        conclusion=research_card["conclusion"],
        keywords=str(research_card["keywords"])
    )

    db.add(paper)
    db.commit()
    db.refresh(paper)
    db.close()

    return{
        "paper_id": paper.id,
        "status": "processed",
        "metadata": {
            "page_count": pdf["page_count"],
            "word_count": pdf["word_count"]
        },
        "research_card": research_card
    }

@app.get("/papers")
def get_papers():
    db=SessionLocal()
    papers=db.query(ResearchCard).all()
    result=[]
    for paper in papers:
        result.append({
            "id": paper.id,
            "title": paper.title,
            "doi": paper.doi,
            "summary": paper.summary,
            "objective": paper.objective,
            "hypothesis": paper.hypothesis,
            "methods": paper.methods,
            "dataset": paper.dataset,
            "research_gap": paper.research_gap,
            "conclusion": paper.conclusion,
            "keywords": paper.keywords,
        })
    db.close()
    return result

@app.post("/chat")
def chat(request: ChatRequest):
    db=SessionLocal()
    papers=db.query(ResearchCard).all()
    db.close()
    if not papers:
        return {"answer": "No research papers uploaded yet! Upload a paper to start asking questions"}
    
    context_blocks=[]
    for paper in papers:
        context_blocks.append(
            f"Title: {paper.title}\nSummary: {paper.summary}\nObjective: {paper.objective}\n"
        )
    context = "\n---\n".join(context_blocks)
    system_prompt=(
        "You are ResearchOS, a sweet, clear, and helpful AI research assistant."
        "Answer the user's question accurately based on the research papers provided in the library context"
        "Keep your response structured, concise, and easy to read."
    )
    response = client.chat.completions.create(
        model="qwen/qwen3-32b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Library Context:\n{context}\n\nQuestion: {request.question}"}
        ],
    )

    return{
        "answer": response.choices[0].message.content
    }