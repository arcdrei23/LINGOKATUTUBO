# LingoKatutubo – Local Running Guide (Windows)

## Prerequisites

- **Python 3.11** — https://www.python.org/downloads/ (check "Add to PATH")
- **Node.js 18+** — https://nodejs.org/
- **Tesseract OCR** *(optional, for scanned-image documents)* —
  https://github.com/UB-Mannheim/tesseract/wiki
  After installing, add `C:\Program Files\Tesseract-OCR` to your system PATH.

---

## Terminal 1 — Backend

```powershell
cd "C:\Users\wapak\Downloads\YAWA\lingokatutubo\backend"

# Create virtual environment (only needed once)
py -3.11 -m venv .venv

# Allow scripts in this PowerShell session
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Start backend server
python -m uvicorn main:app --reload --port 8000
```

Backend URLs:
- API root: http://localhost:8000
- Swagger docs: **http://localhost:8000/docs**
- Health check: http://localhost:8000/health

---

## Terminal 2 — Frontend

```powershell
cd "C:\Users\wapak\Downloads\YAWA\lingokatutubo\frontend"

# Install dependencies (use legacy-peer-deps to avoid peer conflicts)
cmd /c npm install --legacy-peer-deps

# Start frontend dev server
cmd /c npx next dev -p 3000
```

Frontend URL: **http://localhost:3000**

> **Why `cmd /c`?**  PowerShell may block running `npm.cmd`/`.ps1` scripts directly.
> Wrapping with `cmd /c` bypasses that restriction without changing system settings.

---

## Backend API Routes

| Method | URL | Description |
|--------|-----|-------------|
| GET | /health | Health check |
| POST | /translate | Upload document for translation |
| GET | /status/{job_id} | Poll translation progress + detected language |
| GET | /preview/{job_id} | Get preview images |
| GET | /preview-image/{job_id}/{name} | Serve a preview image |
| GET | /download/{job_id} | Download translated PDF |
| POST | /quick-translate | Translate a single phrase |

---

## Supported Languages

| Value | Language | Notes |
|-------|----------|-------|
| `auto` | Auto-Detect | Source only; detects from text |
| `tagabawa` | Bagobo-Tagabawa | Indigenous (dictionary matching) |
| `english` | English | |
| `filipino` | Filipino / Tagalog | |
| `cebuano` | Cebuano | |

---

## Troubleshooting

### PowerShell blocks npm
```powershell
# Option 1: use cmd
cmd /c npm install --legacy-peer-deps
cmd /c npx next dev -p 3000 
# Option 2: allow scripts in this session only
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
npm install --legacy-peer-deps
```

### npm install fails with dependency conflicts
Always add `--legacy-peer-deps`:
```powershell
cmd /c npm install --legacy-peer-deps
```

### "No module named uvicorn"
Make sure the virtual environment is activated before running Python:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### Tailwind CSS not loading (plain text / no colours)
Delete the Next.js cache and restart:
```powershell
Remove-Item -Recurse -Force ".next" -ErrorAction SilentlyContinue
cmd /c npx next dev -p 3000 ```

### Frontend can't reach backend
Make sure both terminals are running simultaneously.
The backend (port 8000) must be active before uploading a document.

### pytesseract errors
Only needed for scanned/image documents.
Install Tesseract OCR and add it to PATH, then restart the terminal.

### Dataset shows no translation
The phrase dataset rows need to be added to `backend/translation_data.json`
under a `"rows"` key (see ARCHITECTURE_DIAGRAM.md for the column schema).
The system will still start and the UI will work; untranslatable words are
returned as-is.

---

## Architecture

```
lingokatutubo/
├── frontend/                    ← Next.js 15 app (React 19, Tailwind v4)
│   ├── app/
│   │   ├── page.tsx             ← Home page
│   │   ├── translate/page.tsx   ← Translator page (4 languages + auto-detect)
│   │   └── about/page.tsx       ← About page
│   ├── components/navigation.tsx
│   ├── hooks/use-upload.ts      ← Calls backend /translate
│   └── lib/utils.ts             ← Tailwind cn() helper
└── backend/                     ← FastAPI (Python 3.11)
    ├── main.py                  ← API routes + CORS
    ├── pipeline_service.py      ← Translation orchestration + auto-detect
    ├── language_detection_service.py ← langdetect + Tagabawa dictionary
    ├── translation_dataset.py   ← Cross-lingual phrase lookup
    ├── translation_data.json    ← Phrase dataset (add "rows" array here)
    └── requirements.txt
```
