class InvoiceError(Exception):
    """Base class for invoice failures."""


class InvalidItemError(InvoiceError):
    pass


class InvalidRateError(InvoiceError):
    pass
