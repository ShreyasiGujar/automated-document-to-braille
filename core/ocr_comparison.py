import fitz
import cv2
import numpy as np
import pytesseract
import easyocr
import time
import re
import unicodedata
from jiwer import wer, cer


print("Loading EasyOCR model...")

reader = easyocr.Reader(['en', 'mr'], gpu=False)

print("Models loaded.\n")


def pdf_to_images(pdf_path):
    images = []
    doc = fitz.open(pdf_path)

    for page in doc:
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))

        img = np.frombuffer(
            pix.samples,
            dtype=np.uint8
        ).reshape(
            pix.height,
            pix.width,
            pix.n
        )

        if pix.n == 4:
            img = cv2.cvtColor(
                img,
                cv2.COLOR_BGRA2BGR
            )

        images.append(img)

    return images


def crop_text_region(img):
    h, w = img.shape[:2]

    x1 = 0
    x2 = w
    y1 = 0
    y2 = h

    return img[y1:y2, x1:x2]


def deskew(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    coords = np.column_stack(
        np.where(gray > 0)
    )

    if len(coords) == 0:
        return image

    angle = cv2.minAreaRect(coords)[-1]

    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)

    M = cv2.getRotationMatrix2D(
        center,
        angle,
        1.0
    )

    rotated = cv2.warpAffine(
        image,
        M,
        (w, h),
        flags=cv2.INTER_CUBIC,
        borderMode=cv2.BORDER_REPLICATE
    )

    return rotated


def preprocess(img):
    img = deskew(img)

    gray = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2GRAY
    )
    kernel = np.array([
        [0, -1, 0],
        [-1, 5,-1],
        [0, -1, 0]
    ])
    
    gray = cv2.filter2D(
        gray,
        -1,
        kernel
    )

    gray = cv2.GaussianBlur(
        gray,
        (5, 5),
        0
    )

    gray = cv2.resize(
        gray,
        None,
        fx=2,
        fy=2,
        interpolation=cv2.INTER_CUBIC
    )
    gray = cv2.fastNlMeansDenoising(
    gray,
    None,
    30,
    7,
    21
    )

    th = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY,
        31,
        2
    )

    kernel = np.ones((2, 2), np.uint8)

    th = cv2.morphologyEx(
        th,
        cv2.MORPH_CLOSE,
        kernel
    )

    return th

def run_tesseract(img):
    config = (
        r'--oem 1 '
        r'--psm 3 '
        r'-l mar+eng '
        r'-c preserve_interword_spaces=1'
    )

    return pytesseract.image_to_string(
        img,
        config=config
    )


def run_easyocr(img):
    result = reader.readtext(
        img,
        detail=0,
        paragraph=True,
        width_ths=0.7,
        height_ths=0.7,
        decoder='beamsearch',
        batch_size=8
    )

    return " ".join(result)

def is_marathi_word(word):
    for ch in word:
        if '\u0900' <= ch <= '\u097F':
            return True
    return False


def score_text(text):
    words = text.split()

    if not words:
        return 0

    valid_words = sum(
        1 for w in words
        if is_marathi_word(w)
    )

    confidence_score = valid_words / len(words)

    bad_chars = sum(
        1 for c in text
        if c in "□?[]|"
    )

    noise_penalty = bad_chars / max(len(text), 1)

    return confidence_score - noise_penalty


COMMON_FIXES = {
    "िो": "हो",
    "िा": "हा",
    "िे": "हे",
    "िी": "ही",
    "जाि": "जात",
    "िोिा": "होता",
    "पाणी": "पाणी",
    "जीवन": "जीवन",
    "बाबा": "बाबा",
    "सुरेश": "सुरेश",
    "मासोळी": "मासोळी"
}


def fix_marathi(text):
    for k, v in COMMON_FIXES.items():
        text = text.replace(k, v)

    return text


def normalize_for_eval(text):
    text = unicodedata.normalize(
        "NFC",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    ).strip()

    text = re.sub(
        r"[^\u0900-\u097Fa-zA-Z0-9\s.,!?;:'\"()\-।]",
        "",
        text
    )

    return text

def trim_to_gt(ocr_text, gt_text):
    gt_wc = len(gt_text.split())

    return " ".join(
        ocr_text.split()[:gt_wc]
    )


def safe_eval(gt, pred):
    if not gt.strip() or not pred.strip():
        return {
            "CER": "N/A",
            "WER": "N/A",
            "Accuracy": "N/A"
        }

    cer_score = cer(gt, pred)
    wer_score = wer(gt, pred)
    accuracy = (1 - cer_score) * 100

    return {
        "CER": round(cer_score * 100, 2),
        "WER": round(wer_score * 100, 2),
        "Accuracy": round(accuracy, 2)
    }


def compare_ocr(pdf_path, ground_truth, pages_to_test=1):
    images = pdf_to_images(pdf_path)
    images = images[:pages_to_test]

    print(f"Testing on {len(images)} page(s)\n")

    tess_text = ""
    easy_text = ""
    hybrid_text = ""

    tess_times = []
    easy_times = []
    hybrid_times = []

    for i, img in enumerate(images):
        try:
            print(f"\nProcessing Page {i+1}")

            text_region = crop_text_region(img)
            processed = preprocess(text_region)

            t0 = time.time()
            tess = run_tesseract(processed)
            tess_times.append(time.time() - t0)
            print("Tesseract done")

            easy = ""
            print("EasyOCR skipped")

            print("\n" + "=" * 60)
            print(f"PAGE {i+1} RAW OCR OUTPUT")
            print("=" * 60)

            print("\nTESSERACT OUTPUT:\n")
            print(tess[:1500])

            print("\n" + "-" * 60)

            print("\nEASYOCR OUTPUT:\n")
            print(easy[:1500])

            print("\n" + "=" * 60 + "\n")

            t0 = time.time()

            tess_score = score_text(tess)
            easy_score = score_text(easy)

            print(f"Tesseract Score: {tess_score}")
            print(f"EasyOCR Score: {easy_score}")
            
            if easy_score > (tess_score + 0.15):
                final = easy
                print("Selected: EasyOCR")
            else:
                final = tess
                print("Selected: Tesseract")

            hybrid_times.append(time.time() - t0)

            print("Hybrid done\n")

            tess_text += tess + " "
            easy_text += easy + " "
            hybrid_text += final + " "
            
        except Exception as e:
            print(f"\nERROR on Page {i+1}")
            print(str(e))
            continue

    tess_text = fix_marathi(tess_text)
    easy_text = fix_marathi(easy_text)
    hybrid_text = fix_marathi(hybrid_text)

    gt_norm = normalize_for_eval(ground_truth)

    tess_norm = trim_to_gt(
        normalize_for_eval(tess_text),
        gt_norm
    )

    easy_norm = trim_to_gt(
        normalize_for_eval(easy_text),
        gt_norm
    )

    hybrid_norm = trim_to_gt(
        normalize_for_eval(hybrid_text),
        gt_norm
    )

    tess_result = safe_eval(gt_norm, tess_norm)
    easy_result = safe_eval(gt_norm, easy_norm)
    hybrid_result = safe_eval(gt_norm, hybrid_norm)

    avg = lambda x: round(sum(x) / len(x), 2)

    print("\n" + "=" * 70)
    print("OCR COMPARISON RESULTS")
    print("=" * 70)

    print(
        f"{'Method':<22}"
        f"{'CER (%)':>10}"
        f"{'WER (%)':>10}"
        f"{'Accuracy':>12}"
        f"{'Time/Page':>15}"
    )

    print("-" * 70)

    print(
        f"{'Tesseract-Only':<22}"
        f"{str(tess_result['CER'])+'%':>10}"
        f"{str(tess_result['WER'])+'%':>10}"
        f"{str(tess_result['Accuracy'])+'%':>12}"
        f"{str(avg(tess_times))+'s':>15}"
    )

    print(
        f"{'EasyOCR-Only':<22}"
        f"{str(easy_result['CER'])+'%':>10}"
        f"{str(easy_result['WER'])+'%':>10}"
        f"{str(easy_result['Accuracy'])+'%':>12}"
        f"{str(avg(easy_times))+'s':>15}"
    )

    print(
        f"{'Hybrid (Proposed)':<22}"
        f"{str(hybrid_result['CER'])+'%':>10}"
        f"{str(hybrid_result['WER'])+'%':>10}"
        f"{str(hybrid_result['Accuracy'])+'%':>12}"
        f"{str(avg(hybrid_times))+'s':>15}"
    )

    print("=" * 70)


if __name__ == "__main__":
    pdf_path = r"C:\Users\gujar\Downloads\bappa_kharech_aahe_ka__swati_vartak_removed.pdf"
    gt_path = r"C:\Users\gujar\OneDrive\Desktop\blind new\data\marathi_scanned\ground_truth.txt"

    with open(
        gt_path,
        "r",
        encoding="utf-8"
    ) as f:
        ground_truth = f.read().strip()

    compare_ocr(
        pdf_path,
        ground_truth,
        pages_to_test=4
    )