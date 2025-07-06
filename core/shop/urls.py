from django.urls import path, re_path
from . import views

app_name = "shop"

urlpatterns = [
    # Route to the product grid page
    path("product/grid/", views.ShopProductGridView.as_view(), name="product-grid"),
    # Route to the product detail page with a dynamic slug
    re_path(
        r"product/(?P<slug>[-\w]+)/detail/",
        views.ShopProductDetailView.as_view(),
        name="product-detail",
    ),

    path("add-or-remove-wishlist/", views.AddOrRemoveWishlistView.as_view(), name="add-or-remove-wishlist"),
]
