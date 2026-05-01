import uuid

from paddleocr import PaddleOCR

ocr = PaddleOCR(use_angle_cls=True, lang="en")


def translate_text(text: str) -> str:
    # Placeholder translator for bilingual output wiring.
    return text


def normalize_bbox(bbox) -> list[float]:
    xs = [point[0] for point in bbox]
    ys = [point[1] for point in bbox]
    return [min(xs), min(ys), max(xs), max(ys)]


def run_ocr(image_path: str) -> dict:
    result = ocr.ocr(image_path, cls=True)
    if not result or not result[0]:
        return {
            "job_id": str(uuid.uuid4()),
            "block_count": 0,
            "results": [],
        }

    blocks = []
    for line in result[0]:
        bbox, (text, confidence) = line
        normalized_bbox = normalize_bbox(bbox)
        blocks.append(
            {
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