import uuid

from shop.enum import OrderStatus
from shop.models import Order
from django.contrib.auth.models import User


class OrderService:

    @staticmethod
    def get_order_by_id(order_id: int, **kwargs) -> Order:
        return Order.objects.prefetch_related('orderline_set').get(id=order_id, **kwargs)

    @classmethod
    def get_pending_order_by_id(cls, order_id: int) -> Order:
        return cls.get_order_by_id(order_id, status=OrderStatus.PENDING.value)

    @staticmethod
    def get_pending_order_by_user(user: User) -> Order:
        if user.is_anonymous:
            raise ValueError("You must use non-anonymous user.")
        return Order.objects.filter(status=OrderStatus.PENDING.value, user=user).order_by('-created_at').first()

    @staticmethod
    def create_pending_order(currency=None, user=None, email=None) -> Order:
        return Order.objects.create(
            status=OrderStatus.PENDING.value,
            number=str(uuid.uuid4()),
            user=user,
            email=email,
            currency=currency,
            total=0
        )
