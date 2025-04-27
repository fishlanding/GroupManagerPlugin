import re

def validate_qq(qq: str) -> bool:
    """Validate QQ number."""
    return bool(re.match(r"^\d{5,12}$", qq))

def validate_duration(duration: str) -> bool:
    """Validate duration is a positive integer."""
    try:
        return int(duration) > 0
    except ValueError:
        return False

def validate_url(url: str) -> bool:
    """Validate URL format."""
    return bool(re.match(r"^https?://[^\s<>]+$", url))