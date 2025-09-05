from app.safety.guard import redact_for_logs, is_denied

def test_redact_email_phone():
    txt = "Contact me at alice@example.com or +1 (415) 555-0100."
    r = redact_for_logs(txt)
    assert "example.com" not in r
    assert "555-0100" not in r
    assert "[REDACTED_EMAIL]" in r
    assert "[REDACTED_PHONE]" in r

def test_denylist_simple():
    assert is_denied("what is my ssn?") is True
    assert is_denied("how to bake a cake?") is False
