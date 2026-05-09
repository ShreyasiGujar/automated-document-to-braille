import re

from core.cleaner import clean_text, preserve_structure
from core.detector import detect_language
from core.normalizer import normalize_marathi
from core.converter import (
    text_to_braille,
    braille_to_text,
    validate_braille
)
from core.marathi_corrector import correct_sentence
from core.logger import log_results
from core.normalizer import final_cleanup


def process_text_pipeline(text, use_ai=False):
    if not text or not text.strip():
        return {
            "clean_text": "",
            "braille_text": "",
            "language": "unknown"
        }

    structured = preserve_structure(text)

    cleaned = clean_text(structured)

    if validate_braille(cleaned):
        cleaned = braille_to_text(cleaned)

    normalized = normalize_marathi(cleaned)

    normalized = final_cleanup(normalized)

    language_info = detect_language(normalized)

    if language_info["marathi"]:
        normalized = correct_sentence(normalized)

    final_text = re.sub(
        r"[^\u0900-\u097FA-Za-z0-9\s.,!?;:'\"()\-\n।]",
        "",
        normalized
    )

    final_text = re.sub(
        r"[ \t]+",
        " ",
        final_text
    )

    final_text = re.sub(
        r"\n{3,}",
        "\n\n",
        final_text
    ).strip()

    braille = text_to_braille(final_text)

    log_results({
        "text_length": len(final_text),
        "language": language_info,
        "braille_detected": validate_braille(text)
    })

    return {
        "clean_text": final_text,
        "braille_text": braille,
        "language": language_info
    }