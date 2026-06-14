# Invoice OCR Pipeline

Automatically extracts structured data from invoice images using Computer Vision and OCR.

## What it does

Upload any invoice image → instantly get vendor, invoice number, dates, tax, and total as structured JSON.

## Tech stack

- **OpenCV** — image preprocessing (grayscale, binarization, denoising)
- **EasyOCR** — deep learning text detection and recognition
- **FastAPI** — REST API endpoint
- **Streamlit** — interactive web UI
- **python-dateutil** — intelligent date format parsing
- **pandas** — data export (JSON, CSV)

## Project structure

```
invoice-ocr-pipeline/
├── ocr_engine.py   # OpenCV preprocessing + EasyOCR
├── extractor.py    # regex field extraction
├── api.py          # FastAPI REST backend
├── app.py          # Streamlit frontend
└── requirements.txt
```

## Run locally

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/invoice-ocr-pipeline.git
cd invoice-ocr-pipeline
```

### 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate  # Mac/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run (two terminals)

**Terminal 1 — API**
```bash
python -m uvicorn api:app --reload
```

**Terminal 2 — UI**
```bash
streamlit run app.py
```

### 5. Open browser

```
http://localhost:8501
```

## API usage

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/extract` | Upload invoice image, returns structured JSON |
| `GET` | `/health` | Health check |

## Sample output

```json
{
  "vendor": "East Repair Inc.",
  "invoice_number": "US-001",
  "date": "2019-02-11",
  "due_date": "2019-02-26",
  "subtotal": 145.0,
  "tax": 9.06,
  "total": 154.06,
  "currency": "USD"
}
```