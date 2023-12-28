from enum import Enum


class CustomEnum(Enum):
    @classmethod
    def choices(cls):
        return [(k.value, k.name) for k in cls]


class OrderStatus(CustomEnum):
    PENDING = 'pending'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'
    SHIPPED = 'shipped'
    DELIVERED = 'delivered'


class Currency(CustomEnum):
    USD = 'USD'
    PLN = 'PLN'
    EUR = 'EUR'
