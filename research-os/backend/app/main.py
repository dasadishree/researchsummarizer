from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

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
    print("Received file:", file.filename)
    print("File size:", len(contents), "bytes")

    return{
        "filename": file.filename,
        "size": len(contents),
        "status": "received"
    }