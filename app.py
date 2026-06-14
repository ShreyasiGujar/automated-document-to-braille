import streamlit as st


st.set_page_config(
    page_title="Braille System",
    layout="wide"
)

import os
import fitz
import cv2
import numpy as np
import pytesseract
import easyocr

from core.extractor import extract_text_from_pdf
from core.pipeline import process_text_pipeline
from output.pdf_generator import generate_pdf


@st.cache_resource
def load_easyocr():
    return easyocr.Reader(['en', 'mr'], gpu=False)

reader = load_easyocr()


##st.set_page_config(page_title="Braille System", layout="wide")
##st.title("Multilingual OCR → Braille (English + Marathi)")


st.sidebar.header("Settings")

input_mode = st.sidebar.radio(
    "Input Type",
    ["Text Input", "Upload PDF"]
)

ocr_mode = st.sidebar.selectbox(
    "OCR Mode",
    ["Hybrid", "Tesseract", "EasyOCR"]
)

use_ai = st.sidebar.checkbox("Enable AI Correction", value=True)


raw_text = ""

if input_mode == "Text Input":
    raw_text = st.text_area("Enter Text", height=200)


elif input_mode == "Upload PDF":

    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

    if uploaded_file is not None:

        file_bytes = uploaded_file.getvalue()
        doc = fitz.open(stream=file_bytes, filetype="pdf")

        if ocr_mode == "Hybrid":
            raw_text = extract_text_from_pdf(uploaded_file)

        else:
            for page in doc:
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)

                if pix.n == 4:
                    img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                if ocr_mode == "Tesseract":
                    config = r'--oem 3 --psm 6'
                    text = pytesseract.image_to_string(gray, lang="mar", config=config)

                else:  # EasyOCR
                    result = reader.readtext(gray, detail=0)
                    text = " ".join(result)

                raw_text += text + "\n"

if st.button("🚀 Process"):

    if not raw_text.strip():
        st.warning("⚠️ No input provided")
    else:

        result = process_text_pipeline(raw_text, use_ai)

        clean_text = result.get("clean_text", "")
        braille_text = result.get("braille_text", "")
        language = result.get("language", "unknown")

        st.success("✅ Processing Complete")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader(f"📝 OCR Output ({ocr_mode})")
            st.text_area(
                "OCR Output",
                raw_text,
                height=300,
                key="ocr_output"
            )

        with col2:
            st.subheader("✨ Cleaned Text")
            st.text_area(
                "Cleaned Text",
                clean_text,
                height=300,
                key="cleaned_text"
            )

        st.subheader("⠿ Braille Output")
        st.text_area(
            "Braille Output",
            braille_text,
            height=200,
            key="braille_output"
        )

        pdf_file = generate_pdf(braille_text)

        if pdf_file and os.path.exists(pdf_file):
            with open(pdf_file, "rb") as f:
                st.download_button(
                    "⬇️ Download Braille PDF",
                    f.read(),
                    "braille_output.pdf"
                )

        st.markdown("### 🔍 Info")
        st.json({
            "language": language,
            "ocr_mode": ocr_mode
        })
