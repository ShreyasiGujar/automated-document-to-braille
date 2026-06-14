import re

def clean_text(text: str) -> str:
    if not text:
        return ""

    # 1. Remove extra spaces (but NOT newlines)
    text = re.sub(r'[ \t]+', ' ', text)

    # 2. Remove unwanted control characters
    text = re.sub(r'[\x00-\x1F\x7F]', '', text)

    # 3. Fix spacing around punctuation
    text = re.sub(r'\s+([.,!?;:])', r'\1', text)

    # 4. Ensure space after punctuation
    text = re.sub(r'([.,!?;:])([^\s])', r'\1 \2', text)

    return text.strip()

def preserve_structure(text: str) -> str:
    if not text:
        return ""

    lines = text.split("\n")

    cleaned = []
    for line in lines:
        line = line.strip()

        # keep empty lines (paragraph breaks)
        if not line:
            cleaned.append("")
        else:
            cleaned.append(line)

    return "\n".join(cleaned)

def remove_noise(text):
    lines = text.split("\n")
    clean_lines = []

    for line in lines:
        line = line.strip()

        if len(line) < 3:
            continue
        if "ई साहित्य" in line:
            continue
        if "©" in line:
            continue
        if "प्रकाशन" in line:
            continue
        if "Whatsapp" in line:
            continue
        if "www." in line:
            continue
        if "gmail" in line.lower():
            continue
        if re.search(r'\d{5,}', line):  # phone numbers
            continue
        if "~~~" in line:
            continue

        clean_lines.append(line)

    return "\n".join(clean_lines)

def fix_repeated_chars(text):
    return re.sub(r'(.)\1{3,}', r'\1\1', text)

def fix_spacing(text):
    text = re.sub(r'\s+([.,!?;:])', r'\1', text)
    text = re.sub(r'([.,!?;:])([^\s])', r'\1 \2', text)
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\s+\)', ')', text)
    return text

def keep_meaningful_text(text):
    lines = text.split("\n")
    result = []

    for line in lines:
        dev_count = sum(1 for c in line if "\u0900" <= c <= "\u097F")

        if dev_count > 5:
            result.append(line)

    return "\n".join(result)

