from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from app.services.pdf_service import extract_text_from_pdf
from app.services.ai_service import create_research_card
app = FastAPI()

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
    
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    pdf = extract_text_from_pdf(contents)
    print("exttracted", pdf["word_count"], "words")
    research_card = create_research_card(pdf["text"])
    print(research_card)
    return{
        "paper_id": "temp-id-123",
        "status": "processed",
        "metadata": {
            "page_count": pdf["page_count"],
            "word_count": pdf["word_count"]
        },
        "research_card": research_card
    }