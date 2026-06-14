<!--
# marathi-and-english-braille-ocr-system
Marathi Braille OCR System converts scanned Marathi and English PDFs into Unicode Braille and emboss-ready Braille PDFs using Tesseract OCR, EasyOCR, text correction, and Bharati Braille mapping. It improves accessibility for visually impaired users through accurate Braille document generation.
-->
# Marathi & English Braille OCR System

A multilingual OCR-to-Braille conversion system that extracts text from images and PDFs, cleans and normalizes the content, detects language (English/Marathi), and converts the output into Bharati Braille.

Built using Python, Streamlit, EasyOCR, Tesseract OCR, and OpenCV.

---

# Features

- OCR extraction from:
  - Images
  - PDFs
- Marathi + English language support
- Text cleaning and normalization pipeline
- Bharati Braille conversion
- Streamlit-based web interface
- PDF export support
- OCR accuracy comparison utilities
- EasyOCR + Tesseract integration

---

# Tech Stack

- Python
- Streamlit
- OpenCV
- EasyOCR
- Tesseract OCR
- PyMuPDF
- NumPy
- FPDF2

---

# Project Structure

```text
marathi-and-english-braille-ocr-system/
│
├── app.py
│
├── core/
│   ├── __init__.py
│   ├── extractor.py
│   ├── pipeline.py
│   ├── cleaner.py
│   ├── detector.py
│   ├── normalizer.py
│   ├── converter.py
│   ├── marathi_corrector.py
│   ├── ai_corrector.py
│   ├── pdf_generator.py
│   └── ocr_comparison.py
│
├── utils/
│   ├── __init__.py
│   ├── constants.py
│   └── logger.py
│
├── data/
│   ├── bharati_braille_map.json
│   └── marathi_matra_map.json
│
├── fonts/
│   └── DejaVuSans.ttf
│
├── requirements.txt
└── README.md
```

---

# Installation

## 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/marathi-and-english-braille-ocr-system.git

cd marathi-and-english-braille-ocr-system
```

---

# 2. Create Virtual Environment (Recommended)

## Windows

```bash
python -m venv venv

venv\Scripts\activate
```

## Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

---

# 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 4. Install Tesseract OCR

This project uses `pytesseract`, which requires the Tesseract OCR engine to be installed separately.

## Windows

Download and install:

https://github.com/UB-Mannheim/tesseract/wiki

After installation, ensure Tesseract is added to PATH.

Example installation path:

```text
C:\Program Files\Tesseract-OCR\tesseract.exe
```

If required, set the path manually inside the project:

```python
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)
```

---

# Running the Application

Start the Streamlit app:

```bash
python -m streamlit run app.py
```

The application will open in your browser automatically.

Default local URL:

```text
http://localhost:8501
```

---

# Supported Input Types

- PNG
- JPG / JPEG
- PDF

---

# Workflow

1. Upload image or PDF
2. OCR extraction using:
   - EasyOCR
   - Tesseract
3. Clean and normalize extracted text
4. Detect language
5. Convert to Bharati Braille
6. Display and export results

---

# Common Issues

## 1. ModuleNotFoundError

Ensure dependencies are installed:

```bash
pip install -r requirements.txt
```

---

## 2. Streamlit Not Found

Run Streamlit using:

```bash
python -m streamlit run app.py
```

instead of:

```bash
streamlit run app.py
```

if Streamlit is not globally available.

---

## 3. Missing Font Error

If you see:

```text
PDF Error: Can't open file fonts/DejaVuSans.ttf
```

Ensure the `fonts/` directory exists and contains:

```text
DejaVuSans.ttf
```

---

## 4. Missing JSON Mapping Files

Ensure these files exist inside `data/`:

```text
bharati_braille_map.json
marathi_matra_map.json
```

---

## 5. Duplicate Streamlit Widget IDs

When using multiple Streamlit widgets of the same type, provide unique keys:

```python
st.text_area(
    "Cleaned Text",
    clean_text,
    key="clean_text_area"
)
```

---

# Requirements

Example dependencies:

```text
streamlit
opencv-python
pytesseract
easyocr
numpy
PyMuPDF
jiwer
fpdf2
Pillow
torch
torchvision
scikit-image
```

---

# Future Improvements

- Better Marathi OCR accuracy
- Audio-to-Braille support
- Multi-page PDF optimization
- Braille preview rendering
- Docker support
- CI/CD integration
- Automated tests
- Model benchmarking dashboard

---

# Contributing

Contributions are welcome.

## Steps

1. Fork the repository
2. Create a new branch

```bash
git checkout -b feature/your-feature-name
```

3. Commit changes

```bash
git commit -m "Add feature"
```

4. Push branch

```bash
git push origin feature/your-feature-name
```

5. Open a Pull Request

---

# License

This project is licensed under the MIT License.


---
