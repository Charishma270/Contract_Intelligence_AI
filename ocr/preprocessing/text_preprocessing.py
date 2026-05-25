import re

def clean_text(text):
    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    # Remove unwanted characters
    text = re.sub(r"[^\w\s.,]", "", text)

    # Normalize dots
    text = re.sub(r"\.+", ".", text)

    return text.strip()