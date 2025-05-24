from django.urls import path

from .. import views


urlpatterns = [
    path("product/list/", views.AdminProductListView.as_view(), name="product-list"),
    path(
        "product/create/", views.AdminProductCreateView.as_view(), name="product-create"
    ),
    path(
        "product/<int:pk>/edit/",
        views.AdminProductEditView.as_view(),
        name="product-edit",
    ),
    path(
        "product/<int:pk>/delete/",
        views.AdminProductDeleteView.as_view(),
        name="product-delete",
    ),
    path("product/<int:pk>/add-extra-image/",views.AdminProductAddExtraImageView.as_view(),name="product-add-extra-image"),
    path("product/<int:pk>/extra-image/<int:image_id>/remove/",views.AdminProductRemoveExtraImageView.as_view(),name="product-remove-extra-image"),
]
