from django import template
from shop.models import ProductModel, ProductStatusType

register = template.Library()

@register.inclusion_tag('includes/latest-products.html')
def show_latest_products(arg=8):
    latest_products = ProductModel.objects.filter(status=ProductStatusType.published.value).order_by('-created_date')[:arg]
    return {'latest_products': latest_products }
