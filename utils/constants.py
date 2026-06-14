from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

LANG_MARATHI = "marathi"
LANG_ENGLISH = "english"
LANG_BRAILLE = "braille"
LANG_UNKNOWN = "unknown"


# Marathi (Devanagari)
MARATHI_RANGE = ("\u0900", "\u097F")

# Braille Unicode
BRAILLE_RANGE = ("\u2800", "\u28FF")



# REGEX PATTERNS
REGEX_MARATHI = r'[\u0900-\u097F]'
REGEX_BRAILLE = r'[\u2800-\u28FF]'
REGEX_ENGLISH = r'[A-Za-z]'


# SUPPORTED LANGUAGES
SUPPORTED_LANGUAGES = [
    LANG_MARATHI,
    LANG_ENGLISH,
    LANG_BRAILLE
]

# FILE SETTINGS
SUPPORTED_FILE_TYPES = ["pdf"]
DEFAULT_OUTPUT_FILE = "braille_output.pdf"


# CLEANING SETTINGS
MAX_REPEAT_CHARS = 3


# OCR SETTINGS
OCR_LANG = "eng+mar"   # Tesseract language pack



# PIPELINE FLAGS
ENABLE_AI_CORRECTION = False   
ENABLE_NORMALIZATION = True


# DEBUG SETTINGS
DEBUG_MODE = True