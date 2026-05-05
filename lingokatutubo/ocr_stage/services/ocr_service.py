import uuid

from paddleocr import PaddleOCR
from services.translator_service import get_translator_service

ocr = PaddleOCR(use_angle_cls=True, lang="en")
translator_service = get_translator_service()


def translate_text(text: str) -> str:
    return translator_service.translate_text(text)


def normalize_bbox(bbox) -> list[float]:
    xs = [point[0] for point in bbox]
    ys = [point[1] for point in bbox]
    return [min(xs), min(ys), max(xs), max(ys)]


def run_ocr(image_path: str, page_number: int = 1) -> dict:
    result = ocr.ocr(image_path, cls=True)
    if not result or not result[0]:
        return {
            "job_id": str(uuid.uuid4()),
            "block_count": 0,
            "results": [],
        }

    blocks = []
    for index, line in enumerate(result[0], start=1):
        bbox, (text, confidence) = line
        normalized_bbox = normalize_bbox(bbox)
        blocks.append(
            {
                "block_id": f"p{page_number}_b{index}",
                "text": text,
                "translation": translate_text(text),
                "bbox": normalized_bbox,
                "confidence": float(confidence),
            }
        )

    return {
        "job_id": str(uuid.uuid4()),
        "block_count": len(blocks),
        "results": blocks,
    }