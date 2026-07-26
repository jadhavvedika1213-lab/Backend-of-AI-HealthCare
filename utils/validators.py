import re
from typing import Optional

EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
PHONE_REGEX = r"^\+?1?\d{9,15}$"

def validate_email_format(email: str) -> bool:
    return bool(re.match(EMAIL_REGEX, email))

def validate_phone_format(phone: str) -> bool:
    return bool(re.match(PHONE_REGEX, phone))

def validate_password_strength(password: str) -> Optional[str]:
    """
    Returns an error message if the password is weak, otherwise None.
    """
    if len(password) < 6:
        return "Password must be at least 6 characters long."
    if not any(char.isdigit() for char in password):
        return "Password must contain at least one digit."
    return None
