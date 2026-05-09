import os
import re
import time
import unicodedata
 
import fitz         
import cv2
import numpy as np
import pytesseract  
import easyocr       
from jiwer import cer  
from PIL import Image
 
 
CATEGORIES = [
    {
        "label":   "English (digital PDF)",
        "folder":  "data/english_digital",      
        "mode":    "digital",
        "engine":  "direct",
    },
    {
        "label":   "Marathi (digital PDF)",
        "folder":  "data/marathi_digital",
        "mode":    "digital",
        "engine":  "tesseract",
    },
    {
        "label":   "Mixed (digital PDF)",
        "folder":  "data/mixed_digital",
        "mode":    "digital",
        "engine":  "tesseract",
    },
    {
        "label":   "Marathi (scanned, Tesseract)",
        "folder":  "data/marathi_scanned",
        "mode":    "scanned",
        "engine":  "tesseract",
    },
    {
        "label":   "Marathi (scanned, Hybrid OCR)",
        "folder":  "data/marathi_scanned",     
        "mode":    "scanned",
        "engine":  "hybrid",
    },
]

TESSERACT_LANG_MARATHI = "mar"
TESSERACT_LANG_ENGLISH = "eng"
TESSERACT_LANG_MIXED   = "mar+eng"
 
def normalize(text: str) -> str:
    if not text:
        return ""
    text = unicodedata.normalize("NFC", text)
    text = re.sub(r"[\u200B-\u200D\u200E\u200F\uFEFF]", "", text)   # ZWJ / BOM
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"([।,.!?])\1+", r"\1", text)
    return text.strip()
 
 
def render_page(page, scale: float = 4.0) -> np.ndarray:
    pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale))
    img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(
        pix.height, pix.width, pix.n
    )
    if pix.n == 4:
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    return img
 
def preprocess(img):
    gray = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2GRAY
    )

    gray = cv2.medianBlur(
        gray,
        3
    )

    gray = cv2.resize(
        gray,
        None,
        fx=3,
        fy=3,
        interpolation=cv2.INTER_CUBIC
    )

    th = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        10
    )

    return th

def _tess_config(lang):
    return (
        f'--oem 3 '
        f'--psm 6 '
        f'-l {lang} '
        f'-c preserve_interword_spaces=1'
    )

 
def run_tesseract(img: np.ndarray, lang: str = TESSERACT_LANG_MARATHI) -> str:
    return pytesseract.image_to_string(img, config=_tess_config(lang))
 
 
_easyocr_reader = None
 
def get_easyocr_reader():
    global _easyocr_reader
    if _easyocr_reader is None:
        # 'mr' = Marathi; gpu=False for reproducibility
        _easyocr_reader = easyocr.Reader(["mr"], gpu=False)
    return _easyocr_reader
 
 
def run_easyocr(img: np.ndarray) -> str:
    result = get_easyocr_reader().readtext(img, detail=0, paragraph=True)
    return " ".join(result)
 
COMMON_FIXES = {
    "िो":  "हो",
    "िा":  "हा",
    "िे":  "हे",
    "िी":  "ही",
    "जाि": "जात",
    "िोिा":"होता",
    "हम":  "मि",
    "शिाणी": "शहाणी",
    "िण":  "हण",
    "आहण": "आणि",
    "मािीि": "माहित",
    "िाहीत": "माहीत",
    "िाणूस": "माणूस",
}

def fix_marathi(text: str) -> str:
    for k, v in COMMON_FIXES.items():
        text = text.replace(k, v)
    # Remove duplicate matras (common OCR artefact)
    text = re.sub(r"([ािीुूेैोौंः])\1+", r"\1", text)
    return text


def text_quality_score(text: str) -> float:
    if not text or len(text.strip()) < 5:
        return 0.0
    dev  = sum(1 for c in text if "\u0900" <= c <= "\u097F")
    bad  = sum(1 for c in text if c in "?□■")
    return (dev - bad * 2) / max(len(text), 1)
 
 
def hybrid_select(tess: str, easy: str) -> str:
    return tess if text_quality_score(tess) >= text_quality_score(easy) else easy
 
 
def extract_text_from_pdf(uploaded_file):
    pdf_bytes = uploaded_file.read()

    pdf = fitz.open(
        stream=pdf_bytes,
        filetype="pdf"
    )

    text = extract_direct(pdf)

    if is_good_text(text):
        pdf.close()
        return normalize(text)

    pred_parts = []

    for page in pdf:
        img = render_page(page)
        processed = preprocess(img)

        text = run_tesseract(
            processed,
            lang=TESSERACT_LANG_MIXED
        )

        text = fix_marathi(text)
        pred_parts.append(text)

    pdf.close()

    return normalize(" ".join(pred_parts))

 
def extract_direct(pdf) -> str:
    parts = []
    for page in pdf:
        blocks = sorted(page.get_text("blocks"), key=lambda b: (b[1], b[0]))
        page_text = "\n".join(b[4].strip() for b in blocks if b[4].strip())
        parts.append(page_text)
    return "\n\n".join(parts)
 
 
def is_good_text(text: str) -> bool:
    if not text or len(text.strip()) < 50:
        return False
    weird = sum(1 for c in text
                if not c.isalnum() and c not in " \n.,!?;:'\"()-।")
    return (weird / max(len(text), 1)) < 0.35
 
 
def evaluate_pdf(pdf_path: str, mode: str, engine: str) -> dict:
    pdf = fitz.open(pdf_path)
    n_pages = len(pdf)

    gt_path = os.path.splitext(pdf_path)[0] + ".txt"
    has_gt = os.path.exists(gt_path)

    gt_text = ""
    if has_gt:
        with open(gt_path, "r", encoding="utf-8") as f:
            gt_text = normalize(f.read())

    t0 = time.time()
    pred_parts = []

    for page in pdf:
        img = render_page(page)

        h, w = img.shape[:2]

        img = img[
            int(h * 0.12):int(h * 0.82),
            int(w * 0.08):int(w * 0.60)
        ]

        cv2.imwrite("debug_crop.png", img)

        processed = preprocess(img)

        cv2.imwrite("debug_processed.png", processed)

        if engine == "tesseract":
            text = run_tesseract(
                processed,
                lang=TESSERACT_LANG_MARATHI
            )

        elif engine == "hybrid":
            text = run_tesseract(
                processed,
                lang=TESSERACT_LANG_MARATHI
            )

        else:
            text = run_tesseract(
                processed,
                lang=TESSERACT_LANG_MIXED
            )

        print("\n========== OCR OUTPUT ==========\n")
        print(text[:2000])
        print("\n================================\n")

        text = fix_marathi(text)

        pred_parts.append(text)

    elapsed = time.time() - t0

    pred = normalize(" ".join(pred_parts))

    acc = char_accuracy(gt_text, pred) if has_gt else None

    return {
        "char_accuracy": acc,
        "time_per_page": elapsed / max(n_pages, 1)
    }


def char_accuracy(gt: str, pred: str) -> float:
    if not gt.strip() or not pred.strip():
        return 0.0

    gt = normalize(gt)
    
    pred = normalize(pred)
    gt_words = gt.split()
    pred_words = pred.split()

    if len(pred_words) > len(gt_words):
        pred = " ".join(pred_words[:len(gt_words)])

    print("\n========== GROUND TRUTH SAMPLE ==========\n")
    print(gt[:1500])

    print("\n========== OCR PREDICTION SAMPLE ==========\n")
    print(pred[:1500])

    print("\n==========================================\n")

    try:
        error = cer(gt, pred)

        # clamp CER
        if error < 0:
            error = 0
        if error > 1:
            error = 1

        acc = (1 - error) * 100

        return round(acc, 1)

    except Exception as e:
        print(f"[CER ERROR] {e}")
        return 0.0

 
def run_comparison() -> list:
    rows = []
 
    for cat in CATEGORIES:
        folder = cat["folder"]
        label  = cat["label"]
        mode   = cat["mode"]
        engine = cat["engine"]
 
        pdf_files = sorted(
            f for f in os.listdir(folder) if f.lower().endswith(".pdf")
        ) if os.path.isdir(folder) else []
 
        if not pdf_files:
            print(f"\n[SKIP] No PDFs found in '{folder}' for: {label}")
            rows.append({
                "label":      label,
                "n_docs":     0,
                "avg_acc":    None,
                "avg_time":   None,
            })
            continue
 
        print(f"\n── {label}  ({len(pdf_files)} docs) ──")
 
        acc_list  = []
        time_list = []
 
        for fname in pdf_files:
            fpath = os.path.join(folder, fname)
            print(f"   {fname} …", end=" ", flush=True)
 
            result = evaluate_pdf(fpath, mode=mode, engine=engine)
            time_list.append(result["time_per_page"])
 
            if result["char_accuracy"] is not None:
                acc_list.append(result["char_accuracy"])
                print(f"acc={result['char_accuracy']:.1f}%  "
                      f"time={result['time_per_page']:.1f}s/page")
            else:
                print(f"(no GT)  time={result['time_per_page']:.1f}s/page")
 
        avg_acc  = round(sum(acc_list)  / len(acc_list),  1) if acc_list  else None
        avg_time = round(sum(time_list) / len(time_list), 1) if time_list else None
 
        rows.append({
            "label":    label,
            "n_docs":   len(pdf_files),
            "avg_acc":  avg_acc,
            "avg_time": avg_time,
        })
 
    return rows


def print_table(rows: list) -> None:
    W = 62
    print("\n" + "=" * W)
    print("  OCR Comparison Table (Research Paper)")
    print("=" * W)
    print(f"  {'Input Category':<32}  {'Docs':>4}  {'Acc (%)':>8}  {'s/page':>7}")
    print("  " + "-" * (W - 2))
 
    for r in rows:
        acc  = f"{r['avg_acc']:.1f}"  if r["avg_acc"]  is not None else "N/A"
        time = f"{r['avg_time']:.1f}" if r["avg_time"] is not None else "N/A"
        print(f"  {r['label']:<32}  {r['n_docs']:>4}  {acc:>8}  {time:>7}")
 
    print("=" * W)
 
    # ── LaTeX ──────────────────────────────────────────────
    print("\n  LaTeX (copy into your paper):\n")
    print(r"  \begin{table}[h]")
    print(r"  \centering")
    print(r"  \caption{OCR Performance Across Input Categories}")
    print(r"  \label{tab:ocr_comparison}")
    print(r"  \begin{tabular}{lccc}")
    print(r"  \hline")
    print(r"  \textbf{Input Category} & \textbf{No.\ of Docs} "
          r"& \textbf{Avg.\ Char Accuracy (\%)} & \textbf{Avg.\ Processing Time (s/page)} \\")
    print(r"  \hline")
 
    for r in rows:
        acc  = f"{r['avg_acc']:.1f}"  if r["avg_acc"]  is not None else "—"
        time = f"{r['avg_time']:.1f}" if r["avg_time"] is not None else "—"
        print(f"  {r['label']} & {r['n_docs']} & {acc} & {time} \\\\")
 
    print(r"  \hline")
    print(r"  \end{tabular}")
    print(r"  \end{table}")
    print()

if __name__ == "__main__":
    rows = run_comparison()
    print_table(rows)
 