# utils/file_handler.py

import email
from email import policy
from email.parser import BytesParser

def read_email_file(file_obj) -> str:
    """
    Reads the content of a .txt or .eml email file and returns clean text.
    
    Args:
        file_obj: Opened file object (binary mode)
    
    Returns:
        str: Extracted plain text content of the email.
    """
    filename = getattr(file_obj, "name", "").lower()

    if filename.endswith(".txt"):
        # Read as plain text
        content = file_obj.read()
        try:
            return content.decode("utf-8")
        except:
            return content.decode("latin-1")

    elif filename.endswith(".eml"):
        # Parse using Python's email module
        msg = BytesParser(policy=policy.default).parse(file_obj)
        parts = []

        # Walk through the email parts
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain":
                parts.append(part.get_content())

        return "\n".join(parts).strip()

    else:
        raise ValueError("Unsupported file type. Only .txt and .eml are supported.")
