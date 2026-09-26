"""
ERP Platform — Domain Exceptions

Base exceptions for domain layer.
Domain exceptions must be explicit and provide useful diagnostic context.
"""

from typing import Any


class DomainException(Exception):
    """Base exception for all domain errors."""

    def __init__(self, message: str, context: dict[str, Any] | None = None):
        self.message = message
        self.context = context or {}
        super().__init__(message)


class EntityNotFoundException(DomainException):
    """Raised when an entity is not found."""

    def __init__(self, entity_type: str, entity_id: Any):
        super().__init__(
            f"{entity_type} not found",
            context={"entity_type": entity_type, "entity_id": str(entity_id)},
        )


class EntityAlreadyExistsException(DomainException):
    """Raised when an entity already exists (duplicate)."""

    def __init__(self, entity_type: str, field: str, value: Any):
        super().__init__(
            f"{entity_type} already exists",
            context={"entity_type": entity_type, "field": field, "value": str(value)},
        )


class AuthorizationException(DomainException):
    """Raised when authorization fails."""

    def __init__(self, message: str = "Unauthorized"):
        super().__init__(message)


class ValidationException(DomainException):
    """Raised when validation fails."""

    def __init__(self, message: str, field: str | None = None):
        context = {"field": field} if field else {}
        super().__init__(message, context=context)


class InsufficientStockException(DomainException):
    """Raised when inventory is insufficient for an operation."""

    def __init__(self, product_id: Any, requested: float, available: float):
        super().__init__(
            f"Insufficient stock for product {product_id}",
            context={
                "product_id": str(product_id),
                "requested": requested,
                "available": available,
            },
        )
