from fastapi import FastAPI, UploadFile, File
import shutil
import os
import uuid
from services.ocr_service import run_ocr

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/ocr")
async def ocr_image(file: UploadFile = File(...)):
    safe_name = f"{uuid.uuid4()}_{os.path.basename(file.filename)}"
    file_path = os.path.join(UPLOAD_DIR, safe_name)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = run_ocr(file_path)

    os.remove(file_path)

    return {
        "filename": file.filename,
        **result
    }