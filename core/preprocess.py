import re
import string
import html

def clean_text(text: str) -> str:
    if not isinstance(text, str):
        text = str(text) if text is not None else ""
    text = re.sub(r"<.*?>", " ", text)
    text = html.unescape(text)
    text = re.sub(r"http\S+|www\S+", " ", text)
    text = re.sub(r"\S+@\S+", " ", text)
    text = re.sub(r"\d+", " ", text)
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = text.lower()
    text = re.sub(r"\s+", " ", text).strip()
    return text

def preprocess_email(email_text: str) -> str:
    return clean_text(email_text)
