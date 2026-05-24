class DomainError(Exception):
    """Base domain error for business rule violations."""


class StockError(DomainError):
    """Raised when inventory rules are violated."""


class OrderStateError(DomainError):
    """Raised when an invalid order state transition is attempted."""
