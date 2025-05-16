from .cart import CartSession


def cart_processor(request):
    """Context processor to inject cart into templates"""
    cart = CartSession(request.session)
    return {"cart": cart}
