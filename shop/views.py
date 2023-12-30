from django.views.generic import ListView
from .models import Product


class ProductListView(ListView):
    model = Product
    page_title = "Welcome to my shop"
    context_object_name = "products"
    paginate_by = 3

    def get_queryset(self):
        return super().get_queryset()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update({"page_title": self.page_title})
        return context
