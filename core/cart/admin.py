from django.contrib import admin

from .models import CartModel, CartItemModel

@admin.register(CartModel)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "created_date", "updated_date")


@admin.register(CartItemModel)
class CartItemModelAdmin(admin.ModelAdmin):
    list_display = ("id", "cart", "product", "quantity")