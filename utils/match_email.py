import re

def extract_email(email: str) -> str:
    sender_email = re.search(r'<(.+?)>', email).group(1) if '<' in email else email

    return sender_email
