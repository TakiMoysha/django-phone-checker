import re


def sanitize_phone(value: str) -> str:
    return re.sub(r"^\+1|[^0-9]+", "", value.strip())
