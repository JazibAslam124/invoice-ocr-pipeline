from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from ocr_engine import run_ocr
from extractor import extract_fields

app = FastAPI(title="Invoice OCR API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post("/extract")
async def extract_invoice(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(400, "Only image files supported")
    image_bytes = await file.read()
    try:
        ocr_lines = run_ocr(image_bytes)
        fields = extract_fields(ocr_lines)
        return {"success": True, "data": fields, "ocr_lines_count": len(ocr_lines)}
    except Exception as e:
        raise HTTPException(500, f"OCR failed: {str(e)}")

@app.get("/health")
async def health():
    return {"status": "ok"}