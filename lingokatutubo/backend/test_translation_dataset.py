"""
Quick smoke-test for TranslationDataset.
Run from the backend directory:
    python test_translation_dataset.py
"""
import sys
import os

# Ensure backend is on the path
sys.path.insert(0, os.path.dirname(__file__))

from translation_dataset import TranslationDataset


def main():
    print("=" * 60)
    print("TranslationDataset smoke test")
    print("=" * 60)

    ds = TranslationDataset()

    print(f"\n[Test] is_loaded : {ds.is_loaded}")
    print(f"[Test] entry count: {len(ds.data)}")

    if not ds.is_loaded:
        print("\n[Test] FAIL: Dataset did not load. Check console output above.")
        print("[Test] Make sure you have one of these files in the backend/ folder:")
        print("       - translation_data.csv  (with columns: tagabawa, english, filipino, ...)")
        print("       - phrasebook.csv")
        print("       - translation_data.json  (with a 'rows' array)")
        sys.exit(1)

    # --- Print first 5 loaded entries ---
    print(f"\n[Test] First 5 loaded entries:")
    for i, row in enumerate(ds.data[:5]):
        en = row.get("english_source", "")
        tg = row.get("tagabawa_source", "")
        fi = row.get("filipino_source", "")
        ce = row.get("cebuano_source", "")
        print(f"  [{i+1}] english={en!r}  tagabawa={tg!r}  filipino={fi!r}  cebuano={ce!r}")

    # --- Test 1: Filipino -> Tagabawa ---
    fi_phrase = ds.data[0].get("filipino_source", "") if ds.data else ""
    fi_expected = ds.data[0].get("tagabawa_source", "") if ds.data else ""
    print(f"\n[Test 1] Filipino -> Tagabawa")
    if fi_phrase:
        result = ds.translate_phrase(fi_phrase, source_lang="filipino", target_lang="tagabawa")
        if result and result != fi_phrase:
            status = "PASS"
        elif result == fi_phrase and fi_expected:
            status = "WARN - returned original (check phrase index)"
        else:
            status = "WARN - no tagabawa translation in dataset for this row"
        print(f"  Input   : {fi_phrase!r}")
        print(f"  Expected: {fi_expected!r}")
        print(f"  Got     : {result!r}  [{status}]")
    else:
        print("  SKIP: no filipino_source in first row")

    # --- Test 2: English -> Tagabawa ---
    en_phrase = ds.data[0].get("english_source", "") if ds.data else ""
    tg_expected = ds.data[0].get("tagabawa_source", "") if ds.data else ""
    print(f"\n[Test 2] English -> Tagabawa")
    if en_phrase:
        result = ds.translate_phrase(en_phrase, source_lang="english", target_lang="tagabawa")
        if result and result != en_phrase:
            status = "PASS"
        elif result == en_phrase and tg_expected:
            status = "WARN - returned original (check phrase index)"
        else:
            status = "WARN - no tagabawa translation in dataset for this row"
        print(f"  Input   : {en_phrase!r}")
        print(f"  Expected: {tg_expected!r}")
        print(f"  Got     : {result!r}  [{status}]")
    else:
        print("  SKIP: no english_source in first row")

    # --- Test 3: Word-by-word partial match ---
    # Try a phrase made of a known word + an unknown word
    known_fi = fi_phrase.split()[0] if fi_phrase else ""
    mixed = f"{known_fi} unknownword999" if known_fi else ""
    print(f"\n[Test 3] Partial word-by-word match")
    if mixed:
        result = ds.translate_phrase(mixed, source_lang="filipino", target_lang="tagabawa")
        has_unknown = "unknownword999" in result
        status = "PASS" if has_unknown else "NOTE - unknown word was changed (unexpected)"
        print(f"  Input   : {mixed!r}")
        print(f"  Got     : {result!r}  [{status}]")
    else:
        print("  SKIP: no filipino words available")

    # --- Test 4: Unknown word fallback ---
    unknown = "xyzzy_nonexistent_word_12345"
    result = ds.translate_phrase(unknown, source_lang="english", target_lang="tagabawa")
    status = "PASS" if result == unknown else "FAIL - unknown word was changed unexpectedly"
    print(f"\n[Test 4] Unknown word fallback (must return original)")
    print(f"  Input   : {unknown!r}")
    print(f"  Got     : {result!r}  [{status}]")

    print("\n" + "=" * 60)
    print("Smoke test complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
