from pypdf import PdfReader
from io import BytesIO

def extract_text_from_pdf(file_bytes: bytes):
    try:
        reader = PdfReader(BytesIO(file_bytes))
        text=""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text+=page_text
        return{
            "text": text,
            "page_count": len(reader.pages),
            "word_count": len(text.split())
        }
    except Exception as e:
        print("pdf parse error:", str(e))
        return{
            "text": "",
            "page_count": 0,
            "word_count": 0,
            "error": str(e)
        }