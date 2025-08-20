## Agentic Document Extraction Challenge – Streamlit App

### Features
- Upload PDFs or images (JPG/PNG)
- Auto route: invoice / medical_bill / prescription (heuristics + LLM fallback)
- OCR via Tesseract; PDF rasterization via PyMuPDF
- LLM extraction to structured JSON with self-consistency voting
- Validation rules (regex/date/amount/totals) and per-field confidence + overall score
- Downloadable JSON and confidence bars in UI

### Dataset
You can use the SROIE receipts dataset (Kaggle). It is suitable for invoices/receipts and works well for this task. For medical bills/prescriptions, feel free to test with your own sample documents.

### Prerequisites (Windows)
1. Python 3.10–3.11 recommended
2. Tesseract OCR (required for image/PDF OCR)
   - Download: https://github.com/UB-Mannheim/tesseract/wiki
   - After install, ensure `tesseract.exe` is on PATH or set `TESSERACT_PATH` in `.env`
3. Microsoft Visual C++ Redistributable (typical dependency for some libs)

### Setup
```bash
python -m venv .venv
. .venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env  # then edit .env to add OPENAI_API_KEY
```

### Run
```bash
streamlit run streamlit_app.py
```

### Config
- Set `OPENAI_API_KEY` in `.env` or Streamlit secrets
- Optional `TESSERACT_PATH` if Tesseract isn’t on PATH

### Project Structure
```
assignment/
  streamlit_app.py
  requirements.txt
  .env.example
  .streamlit/config.toml
  src/
    agent/runner.py
    confidence/scoring.py
    extraction/{extractor.py,schema.py}
    ingest/{ocr.py,pdf_utils.py}
    routing/classifier.py
    utils/json_utils.py
    validation/validators.py
    __init__.py
  data/ (optional)
```

### Notes
- This app prefers OpenAI models (e.g., `gpt-4o-mini`) for extraction. Configure in `src/extraction/extractor.py`.
- Confidence score combines self-consistency agreement, OCR evidence proximity, and validation results.
- Totals validation tries to check that `sum(line_items) ≈ total` within a small tolerance. 