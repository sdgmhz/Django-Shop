from django.views.generic import (ListView,
                                TemplateView,
                                DetailView
)

from .models import ProductModel, ProductStatusType
class ShopProductGridView(ListView):
    template_name = 'shop/product-grid.html'
    queryset = ProductModel.objects.filter(status=ProductStatusType.published.value)