from __future__ import annotations

import csv
import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / "tagabawa_phrasebook_cleaned_auto(phrases).csv"
JSON_PATH = BASE_DIR / "translation_data.json"

EXPECTED_COLUMNS = {
    "topic": ("topic",),
    "tagabawa": ("tagabawa",),
    "english": ("english",),
    "filipino": ("filipino",),
    "cebuano": ("cebuano",),
    "source": ("source",),
    "notes": ("notes",),
}

LEGACY_SOURCE_ENCODINGS = ("cp1252", "latin-1")


def normalize_header(header: str | None) -> str:
    return (header or "").strip().lower()


def ensure_utf8_sig_csv(csv_path: Path) -> str | None:
    try:
        csv_path.read_text(encoding="utf-8-sig")
        return None
    except UnicodeDecodeError:
        raw_bytes = csv_path.read_bytes()

    for encoding in LEGACY_SOURCE_ENCODINGS:
        try:
            decoded = raw_bytes.decode(encoding)
        except UnicodeDecodeError:
            continue

        csv_path.write_text(decoded, encoding="utf-8-sig", newline="")
        return encoding

    raise UnicodeDecodeError(
        "utf-8-sig",
        raw_bytes,
        0,
        min(len(raw_bytes), 1),
        "Unable to decode CSV with supported fallback encodings",
    )


def resolve_column(fieldnames: list[str] | None) -> dict[str, str | None]:
    header_lookup = {normalize_header(name): name for name in fieldnames or []}
    resolved: dict[str, str | None] = {}

    for target_field, variants in EXPECTED_COLUMNS.items():
        resolved[target_field] = next(
            (header_lookup[normalize_header(variant)] for variant in variants if normalize_header(variant) in header_lookup),
            None,
        )

    return resolved


def get_value(row: dict[str, str | None], column_name: str | None) -> str:
    if not column_name:
        return ""
    return (row.get(column_name) or "").strip()


def convert_csv_to_json() -> tuple[int, dict[str, str | None], str | None]:
    if not CSV_PATH.exists():
        raise FileNotFoundError(f"CSV file not found: {CSV_PATH}")

    normalized_from = ensure_utf8_sig_csv(CSV_PATH)

    rows: list[dict[str, object]] = []

    with CSV_PATH.open("r", encoding="utf-8-sig", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        column_map = resolve_column(reader.fieldnames)

        for row in reader:
            topic = get_value(row, column_map["topic"])
            tagabawa = get_value(row, column_map["tagabawa"])
            english = get_value(row, column_map["english"])
            filipino = get_value(row, column_map["filipino"])
            cebuano = get_value(row, column_map["cebuano"])
            source = get_value(row, column_map["source"]) or "phrasebook"
            notes = get_value(row, column_map["notes"])

            if not any((topic, tagabawa, english, filipino, cebuano, notes)):
                continue

            rows.append(
                {
                    "id": len(rows) + 1,
                    "topic": topic,
                    "tagabawa": tagabawa,
                    "english": english,
                    "filipino": filipino,
                    "cebuano": cebuano,
                    "source": source,
                    "notes": notes,
                }
            )

    JSON_PATH.write_text(
        json.dumps({"rows": rows}, ensure_ascii=False, indent=2),
        encoding="utf-8",
        newline="\n",
    )

    return len(rows), column_map, normalized_from


if __name__ == "__main__":
    row_count, column_map, normalized_from = convert_csv_to_json()
    print(f"Created {JSON_PATH.name} with {row_count} rows.")
    print(f"Column map: {column_map}")
    if normalized_from:
        print(f"Normalized CSV encoding from {normalized_from} to utf-8-sig.")
