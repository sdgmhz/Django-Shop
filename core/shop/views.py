from django.views.generic import ListView, TemplateView

class ShopProductGridView(TemplateView):
    template_name = 'shop/product-grid.html'