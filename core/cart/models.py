from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class CartModel(models.Model):
    """Represents a shopping cart for a specific user."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email

class CartItemModel(models.Model):
    """Represents an item inside a shopping cart."""

    cart = models.ForeignKey(CartModel, on_delete=models.CASCADE)
    product = models.ForeignKey("shop.ProductModel", on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=0)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.title} - {self.cart.id}"