import uuid

from paddleocr import PaddleOCR


ocr = PaddleOCR(use_angle_cls=True, lang="en")


def run_ocr(image_path: str) -> dict:
    result = ocr.ocr(image_path, cls=True)

    blocks = []
    for line in result[0]:
        bbox, (text, confidence) = line
        blocks.append(
            {
                "text": text,
                "bbox": bbox,
                "confidence": float(confidence),
            }
        )

    return {
        "job_id": str(uuid.uuid4()),
        "block_count": len(blocks),
        "results": blocks,
    }
from paddleocr import PaddleOCR
import uuid

ocr = PaddleOCR(use_angle_cls=True, lang='en')

def run_ocr(image_path):
    result = ocr.ocr(image_path, cls=True)

    blocks = []
    for line in result[0]:
        bbox, (text, confidence) = line
        blocks.append({
            "text": text,
            "bbox": bbox,
            "confidence": float(confidence)
        })

    return {
        "job_id": str(uuid.uuid4()),
        "block_count": len(blocks),
        "results": blocks
    }   