from openai import OpenAI
import os

client = OpenAI(api_key="OPENAI_API_KEY")


def ai_correct(text: str) -> str:
    if not text or not text.strip():
        return text

    if len(text) < 50:
        return text

    alpha_chars = sum(c.isalpha() for c in text)
    if alpha_chars < len(text) * 0.3:
        return text

    try:
        corrected_text = call_ai_model(text)

        if not corrected_text or not corrected_text.strip():
            return text

        return corrected_text.strip()

    except Exception as e:
        print(f"[AI ERROR] {e}")
        return text


def call_ai_model(text: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Correct grammar and improve clarity. Do not change meaning."},
            {"role": "user", "content": text}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content.strip()
def ai_correct_extraction(text: str) -> str:
    """
    AI correction specifically for extracted text (Marathi-focused)
    """

    if not text or len(text) < 50:
        return text

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Fix OCR errors in Marathi text. Keep original meaning. Do NOT translate. Only correct mistakes."
                },
                {
                    "role": "user",
                    "content": text
                }
            ],
            temperature=0.2
        )

        corrected = response.choices[0].message.content.strip()

        if corrected:
            return "\n".join(line.strip() for line in corrected.split("\n"))
        else:
            return text

    except Exception as e:
        print(f"[AI EXTRACTION ERROR] {e}")
        return text
    
def should_use_ai(text: str) -> bool:
    if not text:
        return False

    alpha = sum(c.isalpha() for c in text)
    digits = sum(c.isdigit() for c in text)
    noise = len(text) - (alpha + digits)

    noise_ratio = noise / len(text)

    return noise_ratio > 0.3