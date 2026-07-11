from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from app.services.pdf_service import extract_text_from_pdf
from app.services.ai_service import create_research_card
from app.database.database import engine, Base, SessionLocal
from app.models import ResearchCard
import app.models

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return{"message": "ResearchOS API is running!"}

@app.get("/papers")
def get_papers():
    db=SessionLocal()
    papers=db.query(ResearchCard).all()
    db.close()
    return papers

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    pdf = extract_text_from_pdf(contents)
    print("exttracted", pdf["word_count"], "words")
    research_card = create_research_card(pdf["text"])
    print(research_card)

    db = SessionLocal()

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
    deb=SessionLocal()
    papers=db.query(ResearchCard).all()
    result=[]
    for paper in papers:
        result.append({
            "id": paper.id,
            "title": paper.title,
            "summary": paper.summary
        })
    db.close()
    return result