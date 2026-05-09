from pathlib import Path
from functools import lru_cache
import re

WORDS_FILE = Path("data/words.txt")

DEV_WORD_RE = re.compile(r"^[\u0900-\u097F]+$")


def load_dictionary():
    if not WORDS_FILE.exists():
        return set()
    with open(WORDS_FILE, "r", encoding="utf-8") as f:
        return {line.strip() for line in f if line.strip()}


DICTIONARY = load_dictionary()


def edit_distance(a, b, limit=1):
    if abs(len(a) - len(b)) > limit:
        return limit + 1

    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        curr = [i]
        row_min = i
        for j, cb in enumerate(b, 1):
            ins = curr[j - 1] + 1
            dele = prev[j] + 1
            sub = prev[j - 1] + (ca != cb)
            val = min(ins, dele, sub)
            curr.append(val)
            row_min = min(row_min, val)
        if row_min > limit:
            return limit + 1
        prev = curr
    return prev[-1]


@lru_cache(maxsize=10000)
def correct_word(word):
    if not word or word in DICTIONARY or not DEV_WORD_RE.match(word):
        return word

    candidates = []
    for w in DICTIONARY:
        if abs(len(w) - len(word)) <= 2:
            d = edit_distance(word, w, limit=1)
            if d <= 2:
                candidates.append((d, len(w), w))

    if not candidates:
        return word

    candidates.sort(key=lambda x: (x[0], len(x[2])))
    return candidates[0][2]


def correct_sentence(text):
    if not text or not DICTIONARY:
        return text

    parts = re.split(r"(\s+)", text)
    out = []
    for part in parts:
        if part.isspace():
            out.append(part)
        elif DEV_WORD_RE.match(part):
            out.append(correct_word(part))
        else:
            out.append(part)
    return "".join(out)