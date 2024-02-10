from django.db.models import QuerySet

from shop.models import Product


class ProductService:
    @staticmethod
    def get_all_products() -> QuerySet[Product]:
        return Product.objects.all().prefetch_related("productprice_set")

    @staticmethod
    def get_product(pk: int) -> Product:
        return Product.objects.get(pk=pk)
