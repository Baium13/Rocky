import uuid
from shop.models import *
from django.contrib.auth.models import User


class OrderService:

    @staticmethod
    def get_order_by_id(order_id: int, **kwargs) -> Order:
        return Order.objects.prefetch_related('orderline_set').get(id=order_id, **kwargs)

    @classmethod
    def get_pending_order_by_id(cls, order_id: int) -> Order:
        return cls.get_order_by_id(order_id, status=OrderStatus.PENDING.value)

    @classmethod
    def get_completed_order_by_id(cls, order_id: int) -> Order:
        return cls.get_order_by_id(order_id, status=OrderStatus.COMPLETED.value)

    @staticmethod
    def get_completed_order_by_user(user: User) -> Order:
        if user.is_anonymous:
            raise ValueError("You must use non-anonymous user.")
        return Order.objects.filter(status=OrderStatus.COMPLETED.value, user=user).order_by('-created_at').first()

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

    @staticmethod
    def get_address(pk: int) -> ShippingAddress:
        return ShippingAddress.objects.get(pk=pk)
