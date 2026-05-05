from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import shutil
import os
import uuid
import fitz
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

    result = run_ocr(file_path, page_number=1)

    os.remove(file_path)

    return {
        "filename": file.filename,
        **result
    }


@app.post("/ocr-pdf")
async def ocr_pdf(file: UploadFile = File(...)):
    if not (file.filename or "").lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    job_id = str(uuid.uuid4())
    safe_name = f"{job_id}_{os.path.basename(file.filename)}"
    pdf_path = os.path.join(UPLOAD_DIR, safe_name)

    with open(pdf_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    pages_dir = os.path.join(UPLOAD_DIR, job_id, "pages")
    os.makedirs(pages_dir, exist_ok=True)

    pages_output = []
    doc = fitz.open(pdf_path)
    try:
        for page_index in range(doc.page_count):
            page = doc[page_index]
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
            image_name = f"page_{page_index + 1}.png"
            image_path = os.path.join(pages_dir, image_name)
            pix.save(image_path)

            ocr_result = run_ocr(image_path, page_number=page_index + 1)
            pages_output.append(
                {
                    "page_number": page_index + 1,
                    "width": float(page.rect.width),
                    "height": float(page.rect.height),
                    "image_url": f"/ocr-page-image/{job_id}/{image_name}",
                    "blocks": ocr_result.get("results", []),
                }
            )
    finally:
        doc.close()
        if os.path.exists(pdf_path):
            os.remove(pdf_path)

    return {
        "job_id": job_id,
        "filename": file.filename,
        "page_count": len(pages_output),
        "pages": pages_output,
    }


@app.get("/ocr-page-image/{job_id}/{image_name}")
async def get_ocr_page_image(job_id: str, image_name: str):
    page_dir = os.path.join(UPLOAD_DIR, job_id, "pages")
    image_path = os.path.join(page_dir, os.path.basename(image_name))

    if not os.path.abspath(image_path).startswith(os.path.abspath(page_dir)):
        raise HTTPException(status_code=403, detail="Access denied.")
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Image not found.")

    return FileResponse(image_path, media_type="image/png")