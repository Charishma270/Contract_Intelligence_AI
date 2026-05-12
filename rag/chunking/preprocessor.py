import re

def clean_text(text):
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text)

    # Remove unwanted symbols
    text = re.sub(r'[^\w\s\.,]', '', text)

    return text.strip()