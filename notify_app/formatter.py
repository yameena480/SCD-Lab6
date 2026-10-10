"""Graded Task 1: reusable notification formatter (email + SMS)."""
from abc import ABC, abstractmethod

SMS_LIMIT = 160  # business rule: single-SMS length


class NotificationFormatter(ABC):
    @abstractmethod
    def format(self, recipient: str, message: str) -> str: ...


class EmailFormatter(NotificationFormatter):
    def format(self, recipient, message):
        if not recipient or not message:
            raise ValueError("recipient and message are required")
        return f"To: {recipient}\nSubject: Notification\n\n{message}"


class SmsFormatter(NotificationFormatter):
    def format(self, recipient, message):
        if not recipient or not message:
            raise ValueError("recipient and message are required")
        text = f"{recipient}: {message}"
        return text if len(text) <= SMS_LIMIT else text[:SMS_LIMIT - 3] + "..."


def notify(formatter: NotificationFormatter, recipient, message, sender=print):
    """I/O is injected (`sender`), so calculation/formatting stay testable."""
    sender(formatter.format(recipient, message))
