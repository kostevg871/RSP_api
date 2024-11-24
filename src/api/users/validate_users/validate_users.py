import re
from typing import Optional

from src.api.users.exceptions_users.exceptions_users import containt_only_letters, email_incorrect

# Регулярное выражение для имени, будет содерать только буквы
LETTER_MATCH_PATTERN = re.compile(
    r'^[a-zA-Z]+$')

# Регулярное выражение для валидации email
EMAIL_REGEX = re.compile(
    r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
)


def validate_name(value: Optional[str]) -> Optional[str]:
    if value is not None and not LETTER_MATCH_PATTERN.match(value):
        containt_only_letters()
    return value


def validate_email(value: Optional[str]) -> Optional[str]:
    if value is not None:
        if not EMAIL_REGEX.match(value):
            email_incorrect()
    return value
