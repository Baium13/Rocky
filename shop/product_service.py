from django.db.models import QuerySet

from shop.models import Product


class ProductService:
    @staticmethod
    def get_all_products() -> QuerySet[Product]:
        return Product.objects.all().prefetch_related("productprice_set")

    @staticmethod
    def get_product_by_upc(upc: int) -> Product:
        return Product.objects.get(upc=upc)

    @staticmethod
    def get_product_by_id(pk: int) -> Product:
        return Product.objects.get(pk=pk)
