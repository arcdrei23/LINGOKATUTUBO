# LingoKatutubo - System Architecture Diagram

## Overall System Flow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           FRONTEND (Next.js + React)                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────────┐  │
│  │  Upload UI   │  │   Progress   │  │   Side-by-Side Viewer        │  │
│  │              │  │    Modal     │  │   ┌──────────┬──────────┐    │  │
│  │  • Drag/Drop │  │              │  │   │ Original │Translated│    │  │
│  │  • File      │  │  Queue ─→    │  │   │   PDF    │   PDF    │    │  │
│  │    Select    │  │  Parse ─→    │  │   │          │          │    │  │
│  │  • Language  │  │  OCR   ─→    │  │   │  Page 1  │  Page 1  │    │  │
│  │    Select    │  │  Trans.─→    │  │   │          │          │    │  │
│  │              │  │  Layout      │  │   └──────────┴──────────┘    │  │
│  └──────┬───────┘  └──────┬───────┘  │   [Toolbar: Pages|Zoom|Download]│
│         │                 │           └────────────────┬─────────────┘  │
│         │                 │                            │                 │
└─────────┼─────────────────┼────────────────────────────┼─────────────────┘
          │                 │                            │
          │ POST /translate │ GET /status/{id}           │ GET /preview/{id}
          ▼                 ▼                            ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        BACKEND API (FastAPI)                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  Endpoints:                                                              │
│  • POST /translate       ─→  Upload & Start Job                         │
│  • GET  /status/{id}     ─→  Poll Job Progress                          │
│  • GET  /preview/{id}    ─→  Get Preview Images                         │
│  • GET  /download/{id}   ─→  Download Translated PDF                    │
│  • GET  /preview-image/{id}/{name} ─→ Serve Preview PNG                 │
│                                                                           │
└───────────────────────────┬─────────────────────────────────────────────┘
                            │
                            │ Async Job Processing
                            ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                       PIPELINE SERVICE                                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  Main Orchestrator: process_translation()                               │
│                                                                           │
│  ┌─────────────────────────────────────────────────────────────┐        │
│  │  Phase 1: Detection (10%)                                   │        │
│  │  ┌────────────────────────────────────────────────┐         │        │
│  │  │ Detection Service                              │         │        │
│  │  │ • detect_pdf_type() ─→ DIGITAL or SCANNED     │         │        │
│  │  └────────────────────────────────────────────────┘         │        │
│  └─────────────────────────────────────────────────────────────┘        │
│                                                                           │
│  ┌─────────────────────────────────────────────────────────────┐        │
│  │  Phase 2: Extraction (25%)                                  │        │
│  │  ┌────────────────────────────────────────────────┐         │        │
│  │  │ Extraction Service (DIGITAL)                   │         │        │
│  │  │ • extract_pdf_with_layout_preservation()       │         │        │
│  │  │   Returns:                                     │         │        │
│  │  │   - Text blocks with coordinates               │         │        │
│  │  │   - Non-text objects (images, lines, shapes)   │         │        │
│  │  │   - Font info, colors, alignment              │         │        │
│  │  └────────────────────────────────────────────────┘         │        │
│  │                         OR                                  │        │
│  │  ┌────────────────────────────────────────────────┐         │        │
│  │  │ OCR Service (SCANNED)                          │         │        │
│  │  │ • process_scanned_pdf()                        │         │        │
│  │  │   - Convert pages to images                    │         │        │
│  │  │   - Run Tesseract OCR                         │         │        │
│  │  │   - Extract text with bounding boxes           │         │        │
│  │  └────────────────────────────────────────────────┘         │        │
│  └─────────────────────────────────────────────────────────────┘        │
│                                                                           │
│  ┌─────────────────────────────────────────────────────────────┐        │
│  │  Phase 3: Language Detection (40%)                          │        │
│  │  ┌────────────────────────────────────────────────┐         │        │
│  │  │ Language Detection Service                     │         │        │
│  │  │ • detect_block_language(text)                  │         │        │
│  │  │   - English, Filipino, Cebuano, Tagabawa       │         │        │
│  │  │   - Confidence scores                          │         │        │
│  │  │   - Handle mixed language                      │         │        │
│  │  └────────────────────────────────────────────────┘         │        │
│  └─────────────────────────────────────────────────────────────┘        │
│                                                                           │
│  ┌─────────────────────────────────────────────────────────────┐        │
│  │  Phase 4: Translation (50-65%)                              │        │
│  │  ┌────────────────────────────────────────────────┐         │        │
│  │  │ Translation Dataset Service                    │         │        │
│  │  │ Strategy Cascade:                              │         │        │
│  │  │                                                │         │        │
│  │  │ 1. Exact Match      ─→ confidence: 1.0        │         │        │
│  │  │    phrase_index lookup                         │         │        │
│  │  │                                                │         │        │
│  │  │ 2. Normalized Match ─→ confidence: 0.95       │         │        │
│  │  │    lowercase, strip punctuation                │         │        │
│  │  │                                                │         │        │
│  │  │ 3. Fuzzy Match      ─→ confidence: 0.7-0.9    │         │        │
│  │  │    fuzzywuzzy similarity > 85%                 │         │        │
│  │  │                                                │         │        │
│  │  │ 4. Dictionary       ─→ confidence: 0.6        │         │        │
│  │  │    DuBois dictionary word lookup               │         │        │
│  │  │                                                │         │        │
│  │  │ 5. Unknown Flag     ─→ confidence: 0.0        │         │        │
│  │  │    [UNKNOWN: text]                             │         │        │
│  │  └────────────────────────────────────────────────┘         │        │
│  │                         +                                   │        │
│  │  ┌────────────────────────────────────────────────┐         │        │
│  │  │ Uncertainty Service                            │         │        │
│  │  │ • Flag low confidence (<0.7)                   │         │        │
│  │  │ • Mark special terms                           │         │        │
│  │  │ • Generate suggestions                         │         │        │
│  │  └────────────────────────────────────────────────┘         │        │
│  └─────────────────────────────────────────────────────────────┘        │
│                                                                           │
│  ┌─────────────────────────────────────────────────────────────┐        │
│  │  Phase 5: PDF Reconstruction (75-85%)                       │        │
│  │  ┌────────────────────────────────────────────────┐         │        │
│  │  │ Reconstruction Service                         │         │        │
│  │  │ • reconstruct_pdf_with_layout()                │         │        │
│  │  │                                                │         │        │
│  │  │   Step 1: Copy Non-Text Objects                │         │        │
│  │  │   ┌────────────────────────────┐               │         │        │
│  │  │   │ • Images  ─→ Same position │               │         │        │
│  │  │   │ • Logos   ─→ Same position │               │         │        │
│  │  │   │ • Lines   ─→ Same position │               │         │        │
│  │  │   │ • Shapes  ─→ Same position │               │         │        │
│  │  │   └────────────────────────────┘               │         │        │
│  │  │                                                │         │        │
│  │  │   Step 2: Insert Translated Text               │         │        │
│  │  │   ┌────────────────────────────┐               │         │        │
│  │  │   │ • Use original coordinates │               │         │        │
│  │  │   │ • Preserve font family     │               │         │        │
│  │  │   │ • Adjust size if needed    │               │         │        │
│  │  │   │ • Keep color & alignment   │               │         │        │
│  │  │   │ • Handle text wrapping     │               │         │        │
│  │  │   └────────────────────────────┘               │         │        │
│  │  └────────────────────────────────────────────────┘         │        │
│  └─────────────────────────────────────────────────────────────┘        │
│                                                                           │
│  ┌─────────────────────────────────────────────────────────────┐        │
│  │  Phase 6: Preview Generation (85-95%)                       │        │
│  │  ┌────────────────────────────────────────────────┐         │        │
│  │  │ Reconstruction Service                         │         │        │
│  │  │ • create_preview_images()                      │         │        │
│  │  │   - Convert PDF pages to PNG                   │         │        │
│  │  │   - Generate for original PDF                  │         │        │
│  │  │   - Generate for translated PDF                │         │        │
│  │  │   - Store in job preview directory             │         │        │
│  │  └────────────────────────────────────────────────┘         │        │
│  └─────────────────────────────────────────────────────────────┘        │
│                                                                           │
│  ┌─────────────────────────────────────────────────────────────┐        │
│  │  Phase 7: Completion (100%)                                 │        │
│  │  • Set job status = "completed"                             │        │
│  │  • Store output paths                                       │        │
│  │  • Return success                                           │        │
│  └─────────────────────────────────────────────────────────────┘        │
│                                                                           │
└─────────────────────────────────────────────────────────────────────────┘


## Data Flow: Layout Preservation

┌─────────────────────────────────────────────────────────────────────────┐
│                          INPUT PDF                                       │
│  ┌─────────────────────────────────────────────────────────┐            │
│  │                                                          │            │
│  │  [LOGO]                                                  │            │
│  │  ══════════════════════════════════════════             │            │
│  │                                                          │            │
│  │  Heading Text Here                                       │            │
│  │                                                          │            │
│  │  This is a paragraph with some text content.            │            │
│  │  It has multiple lines and maintains formatting.         │            │
│  │                                                          │            │
│  │  • Bullet point one                                      │            │
│  │  • Bullet point two                                      │            │
│  │                                                          │            │
│  │        [IMAGE]                                           │            │
│  │                                                          │            │
│  └─────────────────────────────────────────────────────────┘            │
└────────────────────────┬─────────────────────────────────────────────────┘
                         │
                         │ EXTRACTION
                         ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    STRUCTURED PAGE DATA                                  │
├─────────────────────────────────────────────────────────────────────────┤
│  Page 0 (width: 612, height: 792)                                       │
│                                                                           │
│  NON-TEXT OBJECTS (copied as-is):                                       │
│  • image(bbox: [100, 50, 200, 100])    ← Logo                           │
│  • line(bbox: [50, 110, 562, 112])     ← Horizontal line                │
│  • image(bbox: [200, 400, 400, 500])   ← Image                          │
│                                                                           │
│  TEXT BLOCKS (translated):                                              │
│  • block_1(bbox: [50, 130, 300, 150])                                   │
│    text: "Heading Text Here"                                            │
│    font: Arial-Bold, size: 16, color: (0,0,0)                          │
│                                                                           │
│  • block_2(bbox: [50, 170, 562, 210])                                   │
│    text: "This is a paragraph with some text content..."                │
│    font: Arial, size: 11, color: (0,0,0)                               │
│                                                                           │
│  • block_3(bbox: [70, 230, 562, 250])                                   │
│    text: "• Bullet point one"                                           │
│    font: Arial, size: 11, color: (0,0,0)                               │
│                                                                           │
│  • block_4(bbox: [70, 250, 562, 270])                                   │
│    text: "• Bullet point two"                                           │
│    font: Arial, size: 11, color: (0,0,0)                               │
└─────────────────────────────────────────────────────────────────────────┘
                         │
                         │ TRANSLATION
                         ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                       TRANSLATION RESULTS                                │
├─────────────────────────────────────────────────────────────────────────┤
│  "Heading Text Here" ──→ "Pamagat ng Teksto Dito"                       │
│    method: exact, confidence: 1.0                                       │
│                                                                           │
│  "This is a paragraph..." ──→ "Ito ay isang talata..."                  │
│    method: fuzzy, confidence: 0.85                                      │
│                                                                           │
│  "Bullet point one" ──→ "Unang bullet point"                            │
│    method: normalized, confidence: 0.95                                 │
│                                                                           │
│  "Bullet point two" ──→ "Ikalawang bullet point"                        │
│    method: normalized, confidence: 0.95                                 │
└─────────────────────────────────────────────────────────────────────────┘
                         │
                         │ RECONSTRUCTION
                         ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        OUTPUT PDF                                        │
│  ┌─────────────────────────────────────────────────────────┐            │
│  │                                                          │            │
│  │  [LOGO] ← Same position (100, 50, 200, 100)             │            │
│  │  ══════════════════════════════════════════             │            │
│  │         ← Same position (50, 110, 562, 112)             │            │
│  │  Pamagat ng Teksto Dito ← Translated text               │            │
│  │                           Same bbox (50, 130, 300, 150)  │            │
│  │  Ito ay isang talata... ← Translated text                │            │
│  │                          Same bbox (50, 170, 562, 210)   │            │
│  │                                                          │            │
│  │  • Unang bullet point ← Translated                       │            │
│  │  • Ikalawang bullet point                                │            │
│  │                                                          │            │
│  │        [IMAGE] ← Same position (200, 400, 400, 500)      │            │
│  │                                                          │            │
│  └─────────────────────────────────────────────────────────┘            │
└─────────────────────────────────────────────────────────────────────────┘


## Translation Strategy Decision Tree

                    Input: Text Block
                           │
                           ▼
           ┌───────────────────────────────┐
           │  Try Exact Phrase Match       │
           │  phrase_index[text]           │
           └───────────┬───────────────────┘
                       │
                 Found?│       Not Found
                  Yes  │          │
                       ▼          ▼
                ┌──────────┐  ┌──────────────────────┐
                │ Return   │  │ Try Normalized Match │
                │ (conf:   │  │ lowercase, no punct. │
                │  1.0)    │  └──────┬───────────────┘
                └──────────┘         │
                                Found?│       Not Found
                                 Yes  │          │
                                      ▼          ▼
                               ┌──────────┐  ┌──────────────────┐
                               │ Return   │  │ Try Fuzzy Match  │
                               │ (conf:   │  │ similarity > 85% │
                               │  0.95)   │  └──────┬───────────┘
                               └──────────┘         │
                                               Found?│       Not Found
                                                Yes  │          │
                                                     ▼          ▼
                                              ┌──────────┐  ┌────────────────┐
                                              │ Return   │  │ Try Dictionary │
                                              │ (conf:   │  │ word-by-word   │
                                              │ 0.7-0.9) │  └──────┬─────────┘
                                              └──────────┘         │
                                                              Found?│   Not Found
                                                               Yes  │      │
                                                                    ▼      ▼
                                                             ┌──────────┐  ┌────────────┐
                                                             │ Return   │  │ Flag as    │
                                                             │ (conf:   │  │ [UNKNOWN]  │
                                                             │  0.6)    │  │ (conf: 0.0)│
                                                             └──────────┘  └────────────┘


## File Storage Structure

jobs/
  {job_id}/
    ├── input/
    │   └── original.pdf              ← Uploaded file
    ├── structured/
    │   └── layout_data.json          ← Extracted structure
    ├── translated/
    │   └── translations.json         ← Translation results
    ├── output/
    │   ├── translated.pdf            ← Final translated PDF
    │   └── bilingual.pdf             ← Side-by-side version
    └── preview/
        ├── original_page_0.png       ← Preview: Original
        ├── original_page_1.png
        ├── translated_page_0.png     ← Preview: Translated
        └── translated_page_1.png


## Technology Stack

Frontend:
  • Next.js 14+ (React framework)
  • TypeScript
  • Tailwind CSS
  • Lucide React (icons)

Backend:
  • FastAPI (Python web framework)
  • PyMuPDF (fitz) - PDF manipulation
  • python-docx - DOCX handling
  • Pillow - Image processing
  • Tesseract - OCR
  • ReportLab - PDF generation
  • fuzzywuzzy - Fuzzy matching
  • langdetect - Language detection

Storage:
  • Local filesystem (development)
  • S3/GCS (production)

Database:
  • In-memory dict (development)
  • PostgreSQL/MongoDB (production)

Job Queue:
  • asyncio (development)
  • Celery/RQ (production)


## Key Innovation: Layout Preservation

Traditional translation rewrites the entire document.
LingoKatutubo preserves the exact visual layout:

❌ Traditional Approach:
   Extract all text → Translate → Create new document
   Result: Lost layout, no images, reformatted

✅ LingoKatutubo Approach:
   1. Separate text from non-text
   2. Keep non-text at exact positions
   3. Translate only text
   4. Place translated text in original boxes
   Result: Perfect visual match with translated content

This is critical for educational materials where:
  • Diagrams must align with text
  • Cultural symbols stay intact
  • Page structure aids learning
  • Teacher annotations remain valid
