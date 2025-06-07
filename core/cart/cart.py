from shop.models import ProductModel, ProductStatusType
from .models import CartModel, CartItemModel

class CartSession:
    """Session-based cart management"""

    def __init__(self, session):
        """Initialize the cart from session"""
        self.session = session
        self._cart = self.session.setdefault("cart", {"items": []})

    def update_product_quantity(self, product_id, quantity):
        """Update quantity of a product in the cart"""
        for item in self._cart["items"]:
            if product_id == item["product_id"]:
                item["quantity"] = int(quantity)
                break
        else:
            return
        self.save()

    def remove_product(self, product_id):
        """Remove a product from the cart"""
        for item in self._cart["items"]:
            if product_id == item["product_id"]:
                self._cart["items"].remove(item)
                break
        else:
            return
        self.save()

    def add_product(self, product_id):
        """Add a product to the cart or increase its quantity"""
        for item in self._cart["items"]:
            if product_id == item["product_id"]:
                item["quantity"] += 1
                break
        else:
            new_item = {"product_id": product_id, "quantity": 1}

            self._cart["items"].append(new_item)
        self.save()

    def increase_product_quantity(self, product_id):
        """Increase quantity of a product in the cart"""
        for item in self._cart["items"]:
            if product_id == item["product_id"]:
                item["quantity"] += 1
                break
        else:
            return
        self.save()

    def decrease_product_quantity(self, product_id):
        """Decrease quantity of a product in the cart"""
        for item in self._cart["items"]:
            if product_id == item["product_id"]:
                item["quantity"] -= 1
                break
        else:
            return
        self.save()

    def clear(self):
        """Clear the cart"""
        self._cart = self.session["cart"] = {"items": []}
        self.save()

    def get_cart_dict(self):
        """Return raw cart dictionary"""
        return self._cart

    def get_cart_items(self):
        """Return list of cart items enriched with product object and total price"""
        for item in self._cart["items"]:
            product_obj = ProductModel.objects.get(
                id=item["product_id"],
                status=ProductStatusType.published.value,
                stock__gt=0,
            )
            item.update(
                {
                    "product_obj": product_obj,
                    "total_price": item["quantity"] * product_obj.get_price(),
                }
            )

        return self._cart["items"]

    def get_total_payment_amount(self):
        """Calculate total price of all items"""
        return sum(item["total_price"] for item in self._cart["items"])

    def get_total_quantity(self):
        """Calculate total quantity of all items"""
        return sum(item["quantity"] for item in self._cart["items"])

    def save(self):
        """Mark session as modified"""
        self.session.modified = True

    def sync_cart_items_from_db(self, user):
        cart, created = CartModel.objects.get_or_create(user=user)
        cart_items = CartItemModel.objects.filter(cart=cart)
        
        for cart_item in cart_items:
            for item in self._cart["items"]:
                if str(cart_item.product.id) == item["product_id"]:
                    cart_item.quantity = item["quantity"]
                    cart_item.save()
                    break
            else:
                new_item = {"product_id": str(cart_item.product.id), "quantity": cart_item.quantity}
                self._cart["items"].append(new_item)
        self.merge_session_cart_in_db(user)
        self.save()


    def merge_session_cart_in_db(self, user):
        if not user or not user.is_authenticated:
            return
        cart, created = CartModel.objects.get_or_create(user=user)

        for item in self._cart["items"]:
            product_obj = ProductModel.objects.get(
                id=item["product_id"],
                status=ProductStatusType.published.value,
                stock__gt=0,
            )
            cart_item, created = CartItemModel.objects.get_or_create(cart=cart, product=product_obj)
            cart_item.quantity = item["quantity"]

            cart_item.save()

        session_product_ids = [item["product_id"] for item in self._cart["items"]]

        CartItemModel.objects.filter(cart=cart).exclude(product__id__in=session_product_ids).delete()

        
