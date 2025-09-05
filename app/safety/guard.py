"""TODOs:
- redact_for_logs: redact emails and phone numbers from text
- is_denied: simple denylist for disallowed topics (e.g., 'ssn', 'credit card')
"""
import re

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE_RE = re.compile(r"\+?\d[\d\s().-]{7,}\d")  # rough

DENY = {"ssn", "social security number", "credit card", "cvv"}

def redact_for_logs(text: str) -> str:
    # TODO: replace emails with [REDACTED_EMAIL] and phone with [REDACTED_PHONE]
    return text

def is_denied(text: str) -> bool:
    # TODO: return True if any denylist term appears in text (case-insensitive)
    return False
