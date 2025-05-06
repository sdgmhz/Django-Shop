from django import template
from shop.models import ProductModel, ProductStatusType

register = template.Library()


@register.inclusion_tag("includes/latest-products.html")
def show_latest_products(arg=8):
    """Render the latest published products (default: 8 items)"""
    latest_products = ProductModel.objects.filter(
        status=ProductStatusType.published.value
    ).order_by("-created_date")[:arg]
    return {"latest_products": latest_products}


@register.inclusion_tag("includes/similar-products.html")
def show_similar_products(product):
    """Render up to 4 similar products from the same categories"""
    similar_products = (
        ProductModel.objects.filter(
            status=ProductStatusType.published.value,
            category__in=product.category.all(),
        )
        .exclude(id=product.id)
        .order_by("-created_date")
        .distinct()[:4]
    )
    return {"similar_products": similar_products}
