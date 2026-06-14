import re

MARATHI_PATTERN = re.compile(r'[\u0900-\u097F]')
ENGLISH_PATTERN = re.compile(r'[A-Za-z]')


def detect_language(text: str) -> dict:

    result = {
        "marathi": False,
        "english": False,
        "mixed": False
    }

    if not text or not text.strip():
        return result

    has_marathi = bool(MARATHI_PATTERN.search(text))
    has_english = bool(ENGLISH_PATTERN.search(text))

    result["marathi"] = has_marathi
    result["english"] = has_english

    active_languages = sum([has_marathi, has_english])

    if active_languages > 1:
        result["mixed"] = True

    return result


def get_primary_language(text: str) -> str:
    if not text or not text.strip():
        return "unknown"

    marathi_count = len(MARATHI_PATTERN.findall(text))
    english_count = len(ENGLISH_PATTERN.findall(text))

    counts = {
        "marathi": marathi_count,
        "english": english_count
    }

    primary = max(counts, key=counts.get)

    if counts[primary] == 0:
        return "unknown"

    return primary


def detect_full(text: str) -> dict:
    detected = detect_language(text)
    primary = get_primary_language(text)

    return {
        "detected": detected,
        "primary_language": primary
    }