import pytest
from notify_app.formatter import EmailFormatter, SmsFormatter, notify, SMS_LIMIT


def test_email_format():
    out = EmailFormatter().format("a@x.com", "Hello")
    assert out.startswith("To: a@x.com") and out.endswith("Hello")


def test_sms_short_message_unchanged():
    assert SmsFormatter().format("Ali", "Hi") == "Ali: Hi"


def test_sms_truncated_to_limit():
    assert len(SmsFormatter().format("Ali", "x" * 500)) == SMS_LIMIT


@pytest.mark.parametrize("fmt", [EmailFormatter(), SmsFormatter()])
def test_empty_input_rejected(fmt):
    with pytest.raises(ValueError):
        fmt.format("", "msg")


def test_notify_uses_injected_sender():
    sent = []
    notify(SmsFormatter(), "Ali", "Hi", sender=sent.append)
    assert sent == ["Ali: Hi"]
