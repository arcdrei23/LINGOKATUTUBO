from __future__ import annotations

from typing import Dict


UNKNOWN_TOKEN = "UNKNOWN_FOR_REVIEW"


class TranslatorService:
    """
    Lightweight dictionary-based translator for OCR stage output.
    """

    def __init__(self) -> None:
        self._dictionary: Dict[str, str] = {
            "madigar": "Hello",
            "maayong buntag": "Good morning",
            "salamat": "Thank you",
            "oo": "Yes",
            "dili": "No",
        }

    def translate_text(self, text: str) -> str:
        normalized = text.strip().lower()
        if not normalized:
            return UNKNOWN_TOKEN
        return self._dictionary.get(normalized, UNKNOWN_TOKEN)


_translator_service = TranslatorService()


def get_translator_service() -> TranslatorService:
    return _translator_service
