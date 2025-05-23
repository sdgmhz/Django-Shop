from shop.models import ProductModel, ProductStatusType


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
