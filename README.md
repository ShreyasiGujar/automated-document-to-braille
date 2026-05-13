# Marathi and English Braille OCR System

An open source Braille processing and OCR system designed for Marathi and English language support. The project focuses on Braille conversion, text normalization, language correction, and structured output generation for accessibility applications.

---

# Overview

This project provides a complete processing pipeline for:
- Braille validation
- Braille to text conversion
- Text to Braille conversion
- Marathi normalization
- AI based text correction
- Language detection
- PDF output generation

The system is designed to improve accessibility and support digital processing of Marathi and English Braille content.

---

# Features

- Marathi Braille support
- English Braille support
- Braille to text conversion
- Text to Braille conversion
- Marathi language normalization
- AI based text correction
- Structured text preservation
- Language detection
- PDF export support
- Unicode compatible output
- Modular pipeline architecture
- Flask based web interface
- JSON based Braille mappings

---

# Project Structure

```text
marathi-and-english-braille-ocr-system/
│
├── ai_corrector.py              # AI based text correction module
├── app.py                       # Main web application entry point
├── bharati_braille_map.json     # Bharati Braille character mappings
├── braille_output.pdf           # Generated OCR PDF output
├── cleaner.py                   # Cleans and filters OCR output
├── constants.py                 # Stores configurable constants and paths
├── converter.py                 # Converts Braille patterns to readable text
├── DejaVuSans.ttf               # Font used for PDF generation
├── detector.py                  # Detects Braille dots and patterns
├── extractor.py                 # Extracts Braille cells from images
├── marathi_corrector.py         # Marathi language correction module
├── marathi_matra_map.json       # Marathi matra mappings
├── normalizer.py                # Text normalization utilities
├── ocr_comparison.py            # OCR engine comparison utility
├── pdf_generator.py             # Generates embosser-ready PDFs
├── pipeline.py                  # Complete OCR processing pipeline
└── README.md                    # Project documentation
```

---

# File Descriptions

| File Name | Description |
|------------|-------------|
| `ai_corrector.py` | Performs AI based correction and refinement of OCR generated text. |
| `app.py` | Main application entry point responsible for running the web interface. |
| `bharati_braille_map.json` | Stores Bharati Braille mappings for Marathi and English conversion. |
| `braille_output.pdf` | Generated PDF output file containing formatted Braille text. |
| `cleaner.py` | Cleans noisy OCR output and improves formatting consistency. |
| `constants.py` | Stores global constants, configurable parameters, and system settings. |
| `converter.py` | Converts Braille patterns into readable Unicode text. |
| `DejaVuSans.ttf` | Unicode font file used during PDF generation. |
| `detector.py` | Detects Braille patterns and language information. |
| `extractor.py` | Extracts Braille cells and prepares them for processing. |
| `marathi_corrector.py` | Applies Marathi sentence correction and text refinement. |
| `marathi_matra_map.json` | Contains Marathi matra and character mappings. |
| `normalizer.py` | Performs text normalization and cleanup operations. |
| `ocr_comparison.py` | Compares OCR engine outputs and performance. |
| `pdf_generator.py` | Generates structured PDF output from processed text. |
| `pipeline.py` | Controls the complete text processing and Braille conversion workflow. |
| `README.md` | Contains complete project documentation and usage instructions. |

---

# How It Works

The system follows a multi stage text and Braille processing pipeline.

```text
              +------------------+
              |   Input Text     |
              | Braille / Normal |
              +---------+--------+
                        |
                        v
              +------------------+
              | Structure Keeper |
              | preserve_structure()
              +---------+--------+
                        |
                        v
              +------------------+
              | Text Cleaning    |
              | clean_text()     |
              +---------+--------+
                        |
                        v
              +------------------+
              | Braille Validator|
              | validate_braille()|
              +---------+--------+
                        |
          +-------------+-------------+
          |                           |
          v                           v
+------------------+       +------------------+
| Braille to Text  |       | Normal Text Path |
| braille_to_text()|       | Continue Directly|
+---------+--------+       +------------------+
          |
          v
+---------------------------+
| Marathi Normalization     |
| normalize_marathi()       |
+-------------+-------------+
              |
              v
+---------------------------+
| Final Cleanup             |
| final_cleanup()           |
+-------------+-------------+
              |
              v
+---------------------------+
| Language Detection        |
| detect_language()         |
+-------------+-------------+
              |
              v
+---------------------------+
| Marathi Sentence Fixing   |
| correct_sentence()        |
+-------------+-------------+
              |
              v
+---------------------------+
| Character Filtering       |
| Regex Sanitization        |
+-------------+-------------+
              |
              v
+---------------------------+
| Text to Braille           |
| text_to_braille()         |
+-------------+-------------+
              |
              v
+---------------------------+
| Logging & Output          |
| log_results()             |
+---------------------------+
```

---

# Prerequisites

Before running the project, make sure the following is installed:

- Python 3.9 or higher
- pip

Check installation:

```bash
python --version
pip --version
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/aryan-07-code/marathi-and-english-braille-ocr-system.git
```

---

## Move Into Project Directory

```bash
cd marathi-and-english-braille-ocr-system
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Usage

## Run the Web Application

```bash
python app.py
```

After running the command, open:

```text
http://127.0.0.1:5000
```

---

# Application Workflow

1. Upload or enter Marathi / English text or Braille input.
2. The system preserves text structure.
3. Text cleaning and normalization are applied.
4. Braille validation is performed.
5. Marathi correction is applied if Marathi text is detected.
6. Text is converted into Braille representation.
7. Results are generated and exported.

---

# Example Output

```python
{
    "clean_text": "Processed Marathi or English text",
    "braille_text": "⠍⠁⠗⠁⠞⠓⠊",
    "language": {
        "marathi": True,
        "english": False
    }
}
```

---

# Output Features

The system supports:
- Clean normalized text output
- Braille conversion output
- Language detection results
- PDF generation
- Unicode compatible formatting

---

# Troubleshooting

## ModuleNotFoundError

### Problem

A required Python module is missing.

### Fix

Install the missing dependency manually using pip.

Examples:

```bash
pip install flask
```

```bash
pip install reportlab
```

```bash
pip install regex
```

---

## Application Not Starting

### Problem

`app.py` fails to run.

### Fix

Run the application from the project root directory:

```bash
python app.py
```

---

## Marathi Characters Display Incorrectly in PDF

### Problem

Marathi Unicode characters appear broken in generated PDFs.

### Fix

Ensure the `DejaVuSans.ttf` font file exists in the project directory.

---

## Incorrect Output Formatting

### Problem

Output contains unwanted symbols or inconsistent formatting.

### Fix

Check:
- `cleaner.py`
- `normalizer.py`
- `marathi_corrector.py`

---

## Port Already in Use

### Problem

Flask server cannot start because the port is occupied.

### Fix

Run the application on another port:

```bash
flask run --port 5001
```

---

# Future Improvements

- Deep learning based Braille recognition
- Real time webcam support
- Mobile application integration
- Multi language Braille support
- Improved AI correction models
- Cloud deployment support

---

# Contributing

Contributions are welcome.

## Contribution Steps

1. Fork the repository
2. Create a new branch
3. Make changes
4. Commit updates
5. Push the branch
6. Create a Pull Request

---
