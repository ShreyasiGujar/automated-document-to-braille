import re
import unicodedata

def normalize_marathi(text: str) -> str:
    if not text:
        return ""

    text = unicodedata.normalize("NFC", text)

    text = re.sub(r'[\u200B-\u200D\uFEFF]', '', text)

    text = re.sub(r'\s+', ' ', text)

    text = re.sub(r'([.,!?])\1+', r'\1', text)

    text = re.sub(r'[^\u0900-\u097FA-Za-z0-9\s.,!?;:]', '', text)

    return text.strip()


def fix_broken_words(text):
    import re

    # Join split letters across lines
    text = re.sub(r'([\u0900-\u097F])\s*\n\s*([\u0900-\u097F])', r'\1\2', text)

    text = re.sub(r'([क-ह])\s*([ािीुूेैोौंः])', r'\1\2', text)

    text = re.sub(r'([क-ह])\n([क-ह])', r'\1\2', text)

    return text


def fix_matra_order(text):
    text = re.sub(r'([ि])([क-ह])', r'\2\1', text)
    return text


def remove_duplicate_matras(text):
    text = re.sub(r'([ािीुूेैोौंः])\1+', r'\1', text)
    return text

def fix_spacing(text):
    text = re.sub(r'([क-ह])\s+([ािीुूेैोौंः])', r'\1\2', text)

    text = re.sub(r'[ \t]+', ' ', text)

    return text

def final_cleanup(text):
    text = fix_broken_words(text)
    text = fix_matra_order(text)
    text = remove_duplicate_matras(text)
    text = fix_spacing(text)

    text = re.sub(r'\s+', ' ', text).strip()

    return text