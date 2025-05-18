from django.urls import path

from . import views

app_name = "cart"

urlpatterns = [
    # Route to add a product to session cart
    path(
        "session/add-product/",
        views.SessionAddProductView.as_view(),
        name="session-add-product",
    ),
    # Route to remove a product from session cart
    path(
        "session/remove-product/",
        views.SessionRemoveProductView.as_view(),
        name="session-remove-product",
    ),
    # Route to update product quantity in session cart
    path(
        "session/update-product-quantity/",
        views.SessionUpdateProductQuantityView.as_view(),
        name="session-update-product-quantity",
    ),
     # Route to view session cart summary
    path(
        "session/cart/summary/",
        views.SessionCartSummaryView.as_view(),
        name="session-cart-summary",
    ),
    # Route to increase product quantity in session cart
    path(
        "session/increase-product-quantity",
        views.SessionIncreaseProductQuantityView.as_view(),
        name="session-increase-product-quantity",
    ),
    # Route to decrease product quantity in session cart
    path(
        "session/decrease-product-quantity",
        views.SessionDecreaseProductQuantityView.as_view(),
        name="session-decrease-product-quantity",
    ),
]
