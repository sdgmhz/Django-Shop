from django.views.generic import View, TemplateView
from django.http import JsonResponse

from .cart import CartSession


class SessionAddProductView(View):
    """View to add a product to the session-based cart"""

    def post(self, request, *args, **kwargs):
        cart = CartSession(request.session)
        product_id = request.POST.get("product_id")
        if product_id:
            cart.add_product(product_id)
        if request.user.is_authenticated:
            cart.merge_session_cart_in_db(request.user)
        return JsonResponse(
            {"cart": cart.get_cart_dict(), "total_quantity": cart.get_total_quantity()}
        )


class SessionIncreaseProductQuantityView(View):
    """View to increase the quantity of a product in the session cart"""

    def post(self, request, *args, **kwargs):
        cart = CartSession(request.session)
        product_id = request.POST.get("product_id")
        if product_id:
            cart.increase_product_quantity(product_id)
        if request.user.is_authenticated:
            cart.merge_session_cart_in_db(request.user)
        return JsonResponse(
            {"cart": cart.get_cart_dict(), "total_quantity": cart.get_total_quantity()}
        )


class SessionDecreaseProductQuantityView(View):
    """View to decrease the quantity of a product in the session cart"""

    def post(self, request, *args, **kwargs):
        cart = CartSession(request.session)
        product_id = request.POST.get("product_id")
        if product_id:
            cart.decrease_product_quantity(product_id)
        if request.user.is_authenticated:
            cart.merge_session_cart_in_db(request.user)
        return JsonResponse(
            {"cart": cart.get_cart_dict(), "total_quantity": cart.get_total_quantity()}
        )


class SessionRemoveProductView(View):
    """View to remove a product from the session cart"""

    def post(self, request, *args, **kwargs):
        cart = CartSession(request.session)
        product_id = request.POST.get("product_id")
        if product_id:
            cart.remove_product(product_id)
        if request.user.is_authenticated:
            cart.merge_session_cart_in_db(request.user)
        return JsonResponse(
            {"cart": cart.get_cart_dict(), "total_quantity": cart.get_total_quantity()}
        )


class SessionUpdateProductQuantityView(View):
    """View to update the quantity of a product in the session cart"""

    def post(self, request, *args, **kwargs):
        cart = CartSession(request.session)
        product_id = request.POST.get("product_id")
        quantity = request.POST.get("quantity")
        if product_id and quantity:
            cart.update_product_quantity(product_id, quantity)
        if request.user.is_authenticated:
            cart.merge_session_cart_in_db(request.user)
        return JsonResponse(
            {"cart": cart.get_cart_dict(), "total_quantity": cart.get_total_quantity()}
        )


class SessionCartSummaryView(TemplateView):
    """View to display the session cart summary"""

    template_name = "cart/cart-summary.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = CartSession(self.request.session)
        cart_items = cart.get_cart_items()
        context["cart_items"] = cart_items
        context["total_quantity"] = cart.get_total_quantity()
        context["total_payment_price"] = cart.get_total_payment_amount()
        return context
