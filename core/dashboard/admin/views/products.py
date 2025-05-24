from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from django.core.exceptions import FieldError
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages

from dashboard.permissions import HasAdminAccessPermission
from shop.models import ProductModel, ProductCategoryModel, ProductImageModel
from dashboard.admin.forms import ProductForm, ProductExtraImageForm


class AdminProductListView(LoginRequiredMixin, HasAdminAccessPermission, ListView):
    template_name = "dashboard/admin/products/product-list.html"
    paginate_by = 10

    def get_paginate_by(self, queryset):
        """Return the number of products to display per page (based on query parameter)"""
        return self.request.GET.get("page_size", self.paginate_by)

    def get_queryset(self):
        """Return the filtered product list based on query parameters"""
        queryset = ProductModel.objects.all()

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
        return context


class AdminProductEditView(
    LoginRequiredMixin, HasAdminAccessPermission, SuccessMessageMixin, UpdateView
):
    template_name = "dashboard/admin/products/product-edit.html"
    queryset = ProductModel.objects.all()
    form_class = ProductForm
    success_message = "ویرایش محصول با موفقیت انجام شد"

    def get_success_url(self):
        return reverse_lazy(
            "dashboard:admin:product-edit", kwargs={"pk": self.get_object().pk}
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["extra_image_form"] = ProductExtraImageForm()
        return context

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.extra_image.prefetch_related()
        return obj


class AdminProductDeleteView(
    LoginRequiredMixin, HasAdminAccessPermission, SuccessMessageMixin, DeleteView
):
    model = ProductModel
    template_name = "dashboard/admin/products/product-delete.html"
    success_message = "حذف محصول با موفقیت انجام شد"
    success_url = reverse_lazy("dashboard:admin:product-list")


class AdminProductCreateView(
    LoginRequiredMixin, HasAdminAccessPermission, SuccessMessageMixin, CreateView
):
    template_name = "dashboard/admin/products/product-create.html"
    queryset = ProductModel.objects.all()
    form_class = ProductForm
    success_message = "ایجاد محصول با موفقیت انجام شد"

    def form_valid(self, form):
        form.instance.user = self.request.user
        super().form_valid(form)
        return redirect(
            reverse_lazy(
                "dashboard:admin:product-edit", kwargs={"pk": form.instance.pk}
            )
        )

    def get_success_url(self):
        return reverse_lazy("dashboard:admin:product-list")
    

class AdminProductAddExtraImageView(LoginRequiredMixin, HasAdminAccessPermission,SuccessMessageMixin, CreateView):
    http_method_names = ['post']
    form_class = ProductExtraImageForm
    success_message = "تصویر با موفقیت ثبت شد"

    def get_queryset(self):
        return ProductImageModel.objects.filter(product__id=self.kwargs.get('pk'))

    def get_success_url(self):
        return reverse_lazy('dashboard:admin:product-edit', kwargs={'pk': self.kwargs.get('pk')})


    def form_valid(self, form):
        form.instance.product = ProductModel.objects.get(
            pk=self.kwargs.get('pk'))
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, 'اشکالی به وجود آمد. دوباره تلاش کنید.')
        return redirect(reverse_lazy('dashboard:admin:product-edit', kwargs={'pk': self.kwargs.get('pk')}))
    

class AdminProductRemoveExtraImageView(LoginRequiredMixin, HasAdminAccessPermission, SuccessMessageMixin, DeleteView):
    http_method_names = ["post"]
    success_message = "تصویر مورد نظر با موفقیت حذف شد"

    def get_queryset(self):
        return ProductImageModel.objects.filter(product__id=self.kwargs.get('pk'))
    
    def get_object(self, queryset=None):
        return self.get_queryset().get(pk=self.kwargs.get('image_id'))

    def get_success_url(self):
        return reverse_lazy('dashboard:admin:product-edit', kwargs={'pk': self.kwargs.get('pk')})

    def form_invalid(self, form):
        messages.error(
            self.request, 'اشکالی به وجود آمد. دوباره تلاش کنید')
        return redirect(reverse_lazy('dashboard:admin:product-edit', kwargs={'pk': self.kwargs.get('pk')}))
