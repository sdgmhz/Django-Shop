from django import template
from shop.models import ProductModel, ProductStatusType, WishlistProductModel

register = template.Library()


@register.inclusion_tag("includes/latest-products.html", takes_context=True)
def show_latest_products(context, arg=8):
    """Render the latest published products (default: 8 items)"""
    request = context.get("request")
    latest_products = ProductModel.objects.filter(
        status=ProductStatusType.published.value
    ).order_by("-created_date")[:arg]
    wishlist_items = WishlistProductModel.objects.filter(user=request.user).values_list('product__id', flat=True) if request.user.is_authenticated else []
    return {"latest_products": latest_products, "request": request, "wishlist_items": wishlist_items}


@register.inclusion_tag("includes/similar-products.html", takes_context=True)
def show_similar_products(context, product):
    """Render up to 4 similar products from the same categories"""
    request = context.get("request")
    similar_products = (
        ProductModel.objects.filter(
            status=ProductStatusType.published.value,
            category__in=product.category.all(),
        )
        .exclude(id=product.id)
        .order_by("-created_date")
        .distinct()[:4]
    )
    wishlist_items = WishlistProductModel.objects.filter(user=request.user).values_list('product__id', flat=True) if request.user.is_authenticated else []
    return {"similar_products": similar_products, "request": request, "wishlist_items": wishlist_items}
