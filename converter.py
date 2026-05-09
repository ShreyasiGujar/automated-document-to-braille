from pathlib import Path
import json
import re

from utils.constants import BASE_DIR

DATA_DIR = BASE_DIR / "data"

BRAILLE_MAP_PATH = DATA_DIR / "bharati_braille_map.json"
MATRA_MAP_PATH = DATA_DIR / "marathi_matra_map.json"

def _load_json(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"Missing mapping file: {path}")

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


BRAILLE_MAP = _load_json(BRAILLE_MAP_PATH)
MATRA_MAP = _load_json(MATRA_MAP_PATH)

ENG_MAP = BRAILLE_MAP["english"]["letters"]
ENG_SYMBOLS = BRAILLE_MAP["english"].get("symbols", {})

MAR_VOWELS = BRAILLE_MAP["marathi"]["vowels"]
MAR_CONSONANTS = BRAILLE_MAP["marathi"]["consonants"]
MAR_SYMBOLS = BRAILLE_MAP["marathi"].get("symbols", {})

MATRAS = MATRA_MAP.get("matras", {})
MODIFIERS = MATRA_MAP.get("modifiers", {})

NUMBER_INDICATOR = BRAILLE_MAP["numbers"]["indicator"]

ENG_DIGITS = BRAILLE_MAP["numbers"]["english_digits"]
MAR_DIGITS = BRAILLE_MAP["numbers"].get("marathi_digits", {})

BRAILLE_TO_ENG = {v: k for k, v in ENG_MAP.items()}
BRAILLE_TO_DIGIT = {v: k for k, v in ENG_DIGITS.items()}

BRAILLE_TO_MAR = {}

for mapping in [MAR_VOWELS, MAR_CONSONANTS]:
    for k, v in mapping.items():
        BRAILLE_TO_MAR[v] = k

def _symbol_braille(mapping, ch):
    value = mapping.get(ch)

    if value is None:
        return None

    if isinstance(value, dict):
        return value.get("braille")

    return value

def _braille_from_matra(ch):
    info = MATRAS.get(ch)

    if not info:
        return None, "post"

    if isinstance(info, dict):
        return info.get("braille"), info.get("type", "post")

    return info, "post"

def _braille_from_modifier(ch):
    info = MODIFIERS.get(ch)

    if not info:
        return None

    if isinstance(info, dict):
        return info.get("braille")

    return info


def _is_devanagari_consonant(ch):
    return ch in MAR_CONSONANTS

def text_to_braille(text: str) -> str:
    if not text:
        return ""

    output = []
    i = 0
    n = len(text)

    while i < n:
        ch = text[i]

        if ch.isspace():
            output.append(" ")
            i += 1
            continue

        if ch.isdigit() or ch in MAR_DIGITS:
            output.append(NUMBER_INDICATOR)

            while i < n and (
                text[i].isdigit() or text[i] in MAR_DIGITS
            ):
                digit = text[i]

                if digit in ENG_DIGITS:
                    output.append(
                        ENG_DIGITS[digit]
                    )

                elif digit in MAR_DIGITS:
                    output.append(
                        MAR_DIGITS[digit]
                    )

                i += 1

            continue

        if _is_devanagari_consonant(ch):
            braille_seq = MAR_CONSONANTS[ch]
            i += 1

            while i < n and (
                text[i] in MATRAS or
                text[i] in MODIFIERS
            ):
                next_ch = text[i]

                if next_ch in MATRAS:
                    matra_braille, matra_type = _braille_from_matra(next_ch)

                    if matra_braille:
                        if matra_type == "pre":
                            braille_seq = (
                                matra_braille + braille_seq
                            )
                        else:
                            braille_seq += matra_braille

                elif next_ch in MODIFIERS:
                    modifier_braille = _braille_from_modifier(next_ch)

                    if modifier_braille:
                        braille_seq += modifier_braille

                i += 1

            output.append(braille_seq)
            continue


        if ch in MAR_VOWELS:
            output.append(
                MAR_VOWELS[ch]
            )
            i += 1
            continue

        lower = ch.lower()

        if lower in ENG_MAP:
            output.append(
                ENG_MAP[lower]
            )
            i += 1
            continue

        sym = _symbol_braille(
            ENG_SYMBOLS,
            ch
        )

        if sym is not None:
            output.append(sym)
            i += 1
            continue

        sym = _symbol_braille(
            MAR_SYMBOLS,
            ch
        )

        if sym is not None:
            output.append(sym)
            i += 1
            continue

        i += 1

    result = "".join(output)

    result = re.sub(
        r"\s{2,}",
        " ",
        result
    ).strip()

    return result

def braille_to_text(text: str) -> str:
    if not text:
        return ""

    output = []
    i = 0
    n = len(text)

    reverse_map = {}

    for mapping in [MAR_VOWELS, MAR_CONSONANTS]:
        for k, v in mapping.items():
            reverse_map[v] = k

    for k, v in MAR_SYMBOLS.items():
        reverse_map[v] = k

    for k, v in ENG_MAP.items():
        reverse_map[v] = k

    sorted_keys = sorted(
        reverse_map.keys(),
        key=len,
        reverse=True
    )

    while i < n:
        matched = False

        if text[i] == NUMBER_INDICATOR:
            i += 1

            while i < n and text[i] in BRAILLE_TO_DIGIT:
                output.append(
                    BRAILLE_TO_DIGIT[text[i]]
                )
                i += 1

            continue

        for key in sorted_keys:
            if text[i:i + len(key)] == key:
                output.append(
                    reverse_map[key]
                )

                i += len(key)
                matched = True
                break

        if not matched:
            output.append(text[i])
            i += 1

    final = "".join(output)

    final = re.sub(
        r"\s{2,}",
        " ",
        final
    ).strip()

    return final


def validate_braille(text: str) -> bool:
    if not text:
        return False

    braille_chars = sum(
        1 for c in text
        if "\u2800" <= c <= "\u28FF"
    )

    total_chars = len(text)

    if total_chars == 0:
        return False

    ratio = braille_chars / total_chars

    return ratio > 0.30