from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, UpdateView, DeleteView, CreateView, DetailView
from django.core.exceptions import FieldError
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect

from dashboard.permissions import HasAdminAccessPermission
from order.models import CouponModel 
from dashboard.admin.forms import CouponForm


class AdminCouponListView(LoginRequiredMixin, HasAdminAccessPermission, ListView):
    template_name = "dashboard/admin/coupons/coupon-list.html"
    paginate_by = 10

    def get_paginate_by(self, queryset):
        """Return the number of coupons to display per page (based on query parameter)"""
        return self.request.GET.get("page_size", self.paginate_by)

    def get_queryset(self):
        """Return the filtered coupons list based on query parameters"""
        queryset = CouponModel.objects.all()

        # Filter by search query if provided
        if search_q := self.request.GET.get("q"):
            queryset = queryset.filter(code__icontains=search_q)

        # Order by the provided field, if valid
        if order_by := self.request.GET.get("order_by"):
            try:
                queryset = queryset.order_by(order_by)
            except FieldError:
                pass

        return queryset

    def get_context_data(self, **kwargs):
        """Add additional context (total item count) to the context"""
        context = super().get_context_data(**kwargs)
        context["total_items"] = self.get_queryset().count()  
        return context


class AdminCouponEditView(
    LoginRequiredMixin, HasAdminAccessPermission, SuccessMessageMixin, UpdateView
):
    template_name = "dashboard/admin/coupons/coupon-edit.html"
    queryset = CouponModel.objects.all()
    form_class = CouponForm
    success_message = "ویرایش کد تخفیف با موفقیت انجام شد"

    def get_success_url(self):
        return reverse_lazy(
            "dashboard:admin:coupon-edit", kwargs={"pk": self.get_object().pk}
        )


class AdminCouponDeleteView(
    LoginRequiredMixin, HasAdminAccessPermission, SuccessMessageMixin, DeleteView
):
    model = CouponModel
    template_name = "dashboard/admin/coupons/coupon-delete.html"
    success_message = "حذف کد تخفیف با موفقیت انجام شد"
    success_url = reverse_lazy("dashboard:admin:coupon-list")


class AdminCouponCreateView(
    LoginRequiredMixin, HasAdminAccessPermission, SuccessMessageMixin, CreateView
):
    template_name = "dashboard/admin/coupons/coupon-create.html"
    queryset = CouponModel.objects.all()
    form_class = CouponForm
    success_message = "ایجاد کد تخفیف با موفقیت انجام شد"

    def form_valid(self, form):
        form.instance.user = self.request.user
        super().form_valid(form)
        return redirect(
            reverse_lazy(
                "dashboard:admin:coupon-edit", kwargs={"pk": form.instance.pk}
            )
        )

    def get_success_url(self):
        return reverse_lazy("dashboard:admin:coupon-list")
    

class AdminCouponUsersView(LoginRequiredMixin, HasAdminAccessPermission,DetailView):
    template_name = "dashboard/admin/coupons/coupon-users.html"
    queryset = CouponModel.objects.all()