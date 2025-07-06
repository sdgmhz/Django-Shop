from django.views.generic import ListView, DetailView, View
from django.core.exceptions import FieldError
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

from .models import ProductModel, ProductStatusType, ProductCategoryModel, WishlistProductModel
from cart.cart import CartSession


class ShopProductGridView(ListView):
    """View to display a grid of products with pagination and filters"""

    template_name = "shop/product-grid.html"
    paginate_by = 9

    def get_paginate_by(self, queryset):
        """Return the number of products to display per page (based on query parameter)"""
        return self.request.GET.get("page_size", self.paginate_by)

    def get_queryset(self):
        """Return the filtered product list based on query parameters"""
        queryset = ProductModel.objects.filter(status=ProductStatusType.published.value)

        # Filter by search query if provided
        if search_q := self.request.GET.get("q"):
            queryset = queryset.filter(title__icontains=search_q)

        # Filter by category if provided
        if category_id := self.request.GET.get("category_id"):
            queryset = queryset.filter(category__id=category_id)

        # Filter by minimum price if provided
        if min_price := self.request.GET.get("min_price"):
            queryset = queryset.filter(price__gte=min_price)

        # Filter by maximum price if provided
        if max_price := self.request.GET.get("max_price"):
            queryset = queryset.filter(price__lte=max_price)

        # Order by the provided field, if valid
        if order_by := self.request.GET.get("order_by"):
            try:
                queryset = queryset.order_by(order_by)
            except FieldError:
                pass

        return queryset

    def get_context_data(self, **kwargs):
        """Add additional context (total item count and categories) to the context"""
        context = super().get_context_data(**kwargs)
        context["total_items"] = self.get_queryset().count()  # Total products count
        context["categories"] = (
            ProductCategoryModel.objects.all()
        )  # List of all product categories
        context["wishlist_items"] = WishlistProductModel.objects.filter(user=self.request.user).values_list('product__id', flat=True) if self.request.user.is_authenticated else []
        return context


class ShopProductDetailView(DetailView):
    """View to display details of a specific product"""

    template_name = "shop/product-detail.html"
    queryset = ProductModel.objects.filter(
        status=ProductStatusType.published.value
    )  # Only published products

    def get_context_data(self, **kwargs):
        """Add additional context (matching item) to the context"""
        context = super().get_context_data(**kwargs)
        cart = CartSession(self.request.session)
        cart_items = cart.get_cart_items()
        matching_item = next(
            (item for item in cart_items if int(item["product_id"]) == self.object.id),
            None,
        )
        context["matching_item"] = matching_item
        context["is_wished"] = WishlistProductModel.objects.filter(user=self.request.user, product__id=self.get_object().id).exists() if self.request.user.is_authenticated else False
        return context
    

class AddOrRemoveWishlistView(LoginRequiredMixin,View):

    def post(self, request, *args, **kwargs):
        product_id = request.POST.get("product_id")
        message = ""
        if product_id:
            try:
                wishlist_item = WishlistProductModel.objects.get(user=request.user, product__id=product_id)
                wishlist_item.delete()
                message = "محصول از لیست علایق شما حذف شد"
            except WishlistProductModel.DoesNotExist:
                WishlistProductModel.objects.create(user=request.user, product_id=product_id)
                message = "محصول به لیست علایق شما اضافه شد"
            
        return JsonResponse({"message":message})


