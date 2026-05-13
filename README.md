# Marathi and English Braille OCR System

An open source Optical Character Recognition (OCR) system designed to recognize and process Marathi and English Braille documents. This project focuses on improving accessibility by converting Braille patterns into readable digital text using image processing and OCR techniques.

---

# Overview

This project provides a complete pipeline for detecting, extracting, and converting Braille characters from images into readable Marathi and English text. It is intended for:

- Developers working on accessibility solutions
- Researchers in OCR and assistive technology
- Students exploring computer vision and machine learning
- Organizations supporting visually impaired communities

The system combines image preprocessing, Braille segmentation, OCR mapping, and text generation into a modular workflow.

---

# Features

- Marathi Braille recognition
- English Braille recognition
- Image preprocessing pipeline
- Noise reduction and enhancement
- Braille dot detection
- Character segmentation
- OCR engine integration
- Unicode text output
- PDF export support
- Embosser-ready formatting
- Modular architecture
- Easy configuration through constants/config files
- Web interface support
- CLI execution support
- OCR engine comparison support
- Open source and customizable

---

# System Architecture

```text
                +-------------------+
                | Input Braille Img |
                +---------+---------+
                          |
                          v
                +-------------------+
                | Image Preprocess  |
                | Resize / Denoise  |
                +---------+---------+
                          |
                          v
                +-------------------+
                | Braille Detection |
                | Dot Extraction    |
                +---------+---------+
                          |
                          v
                +-------------------+
                | Character Mapping |
                | Marathi / English |
                +---------+---------+
                          |
                          v
                +-------------------+
                | OCR Processing    |
                +---------+---------+
                          |
                          v
                +-------------------+
                | Text Generation   |
                +---------+---------+
                          |
                          v
                +-------------------+
                | Output Export     |
                | TXT / PDF / JSON  |
                +-------------------+
```

---

# Project Structure

```
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
| `ai_corrector.py` | Performs AI based correction and refinement of OCR generated text to improve recognition accuracy. |
| `app.py` | Main application entry point responsible for running the web interface and handling user interaction. |
| `bharati_braille_map.json` | Contains Bharati Braille mappings used for converting Braille patterns into readable Marathi and English characters. |
| `braille_output.pdf` | Generated PDF output file containing the final recognized and formatted Braille text. |
| `cleaner.py` | Cleans noisy OCR output, removes unwanted symbols, and improves text formatting consistency. |
| `constants.py` | Stores global constants, configurable parameters, paths, thresholds, and system settings used across the project. |
| `converter.py` | Converts extracted Braille dot patterns into corresponding Unicode text characters. |
| `DejaVuSans.ttf` | Font file used during PDF generation to support Unicode Marathi and English characters correctly. |
| `detector.py` | Detects Braille dots and identifies Braille cell structures from processed images. |
| `extractor.py` | Extracts segmented Braille cells and prepares them for OCR mapping and conversion. |
| `marathi_corrector.py` | Performs Marathi specific language correction and improves sentence level text accuracy. |
| `marathi_matra_map.json` | Stores Marathi matra mappings and language specific character relationships for accurate conversion. |
| `normalizer.py` | Normalizes OCR output text by standardizing spacing, symbols, and character formatting. |
| `ocr_comparison.py` | Compares OCR engines such as Tesseract and EasyOCR for performance, speed, and accuracy evaluation. |
| `pdf_generator.py` | Generates structured and embosser-ready PDF files from the final OCR processed text. |
| `pipeline.py` | Controls the complete OCR workflow including preprocessing, detection, extraction, conversion, correction, and output generation. |
| `README.md` | Contains complete project documentation, installation guide, usage instructions, and contributor information. |

---

# How It Works

The system follows a multi stage text and Braille processing pipeline designed for Marathi and English Braille conversion, correction, and normalization.

---

## Processing Pipeline

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

# Pipeline Stages

## 1. Structure Preservation

The input text structure is preserved before cleaning begins.  
This helps maintain:
- line breaks
- paragraph formatting
- spacing consistency

Function used:

```python
preserve_structure()
```

---

## 2. Text Cleaning

Noise, unwanted symbols, and malformed characters are removed.

Function used:

```python
clean_text()
```

---

## 3. Braille Validation

The system checks whether the input already contains Braille patterns.

Function used:

```python
validate_braille()
```

If Braille is detected:
- Braille is converted back into readable text
- Processing continues on normalized text

---

## 4. Marathi Normalization

Marathi Unicode inconsistencies and formatting problems are corrected.

Function used:

```python
normalize_marathi()
```

---

## 5. Final Cleanup

Additional cleanup removes:
- extra whitespace
- invalid formatting
- repeated line breaks

Function used:

```python
final_cleanup()
```

---

## 6. Language Detection

The pipeline identifies whether the text contains:
- Marathi
- English
- mixed language content

Function used:

```python
detect_language()
```

---

## 7. Marathi Sentence Correction

If Marathi text is detected, sentence level correction is applied.

Function used:

```python
correct_sentence()
```

This improves:
- spelling consistency
- sentence readability
- OCR correction quality

---

## 8. Character Sanitization

Regex based filtering removes unsupported symbols while preserving:
- Marathi Unicode characters
- English alphabets
- numbers
- punctuation

---

## 9. Braille Conversion

The cleaned text is converted into Braille representation.

Function used:

```python
text_to_braille()
```

---

## 10. Logging & Result Generation

The system logs:
- text length
- language information
- Braille detection results

Function used:

```python
log_results()
```

The final pipeline output includes:

```python
{
    "clean_text": final_text,
    "braille_text": braille,
    "language": language_info
}
```
---

# Prerequisites

## Python

- Python 3.9+
- pip
- virtualenv recommended

---

# Install Tesseract OCR

## Ubuntu

```bash
sudo apt update
sudo apt install tesseract-ocr
```

## macOS

```bash
brew install tesseract
```

## Windows

1. Download installer from:
https://github.com/UB-Mannheim/tesseract/wiki

2. Add Tesseract path to environment variables.

Example:

```text
C:\Program Files\Tesseract-OCR
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/aryan-07-code/marathi-and-english-braille-ocr-system.git
```

## Move Into Project

```bash
cd marathi-and-english-braille-ocr-system
```

## Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux/macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

## Install Dependencies Manually

Install the required Python libraries:

```bash
pip install flask regex reportlab
```

If additional modules are used in your environment, install them similarly using `pip`.

---

## Run the Application

```bash
python app.py
```

---

# Usage

## Run the Web Application

Start the Flask application:

```bash
python app.py
```

After running the command, open the local server URL shown in the terminal, usually:

```text
http://127.0.0.1:5000
```

---

# Application Workflow

1. Upload or enter Marathi / English text or Braille input.
2. The system cleans and normalizes the text.
3. Braille patterns are validated and processed.
4. Marathi language correction is applied if detected.
5. Clean text is converted into Braille representation.
6. Output is generated and exported as formatted text or PDF.

---

# Output

The system generates:

- Clean normalized text
- Braille converted output
- Language detection results
- PDF output support

Example output:

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

# Configuration

The project uses `constants.py` and JSON configuration files for customization.

Example configurable parameters:

```python
IMAGE_SIZE = (512, 512)
THRESHOLD_VALUE = 127
OCR_ENGINE = "tesseract"
LANGUAGE = "marathi"
EXPORT_PDF = True
```

---

# Output Formats

| Format | Description |
|--------|-------------|
| TXT | Plain recognized text |
| PDF | Embosser-ready formatted PDF |
| JSON | Structured OCR output |

---

# Bharati Braille Standard

This project follows Bharati Braille conventions for Indian languages.

## Sample Mapping

| Braille Pattern | Character |
|----------------|-----------|
| ⠁ | A |
| ⠃ | B |
| ⠉ | C |
| ⠅ | K |
| ⠍ | M |

---

# OCR Engine Comparison

| Feature | Tesseract | EasyOCR |
|---------|-----------|----------|
| Speed | Fast | Medium |
| Accuracy | High | High |
| Marathi Support | Moderate | Better |
| CPU Usage | Low | Medium |
| GPU Support | No | Yes |

---

# Troubleshooting

## Tesseract Not Found

### Fix

Add Tesseract installation path to environment variables.

---

## ModuleNotFoundError

### Problem

A required Python module is missing.

### Fix

Install the missing module manually using pip.

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

If another module is missing, install it using:

```bash
pip install module_name
```

---

## OCR Accuracy Low

### Fix

- Use high resolution images
- Improve lighting conditions
- Apply preprocessing properly

---

## Virtual Environment Issues

### Fix

Delete and recreate the virtual environment.

---

# Contributing

Contributions are welcome.

## Areas Needing Improvement

- OCR accuracy optimization
- Better Marathi Braille datasets
- Deep learning integration
- Improved UI/UX
- Mobile support
- Real-time camera OCR
- Faster preprocessing pipeline

## Contribution Steps

1. Fork repository
2. Create feature branch
3. Commit changes
4. Push branch
5. Create Pull Request

---

# Future Scope

- AI based Braille recognition
- Real-time OCR using webcam
- Mobile application integration
- Speech output generation
- Cloud deployment
- Multi-language Braille support

---
