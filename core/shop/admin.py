from django.contrib import admin
from .models import ProductModel, ProductImageModel, ProductCategoryModel, WishlistProductModel


@admin.register(ProductModel)
class ProductModelAdmin(admin.ModelAdmin):
    """Admin configuration for ProductModel"""

    list_display = (
        "id",
        "title",
        "stock",
        "status",
        "price",
        "discount_percent",
        "created_date",
    )


@admin.register(ProductCategoryModel)
class ProductCategoryModelAdmin(admin.ModelAdmin):
    """Admin configuration for ProductCategoryModel"""

    list_display = (
        "id",
        "title",
        "created_date",
    )


@admin.register(ProductImageModel)
class ProductImageModel(admin.ModelAdmin):
    """Admin configuration for ProductImageModel"""

    list_display = ("id", "file", "created_date")


@admin.register(WishlistProductModel)
class WishlistProductModelAdmin(admin.ModelAdmin):
    """Admin configuration for WishlistProductModel"""

    list_display = ("id", "user", "product")
