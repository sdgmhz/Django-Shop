from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import FieldError


from order.models import OrderModel
from dashboard.permissions import HasCustomerAccessPermission


class CustomerOrderListView(
    LoginRequiredMixin, HasCustomerAccessPermission, ListView
):
    template_name = "dashboard/customer/orders/order-list.html"

    paginate_by = 5

    def get_paginate_by(self, queryset):
        """Return the number of products to display per page (based on query parameter)"""
        return self.request.GET.get("page_size", self.paginate_by)

    def get_queryset(self):
        queryset = OrderModel.objects.filter(user=self.request.user)
        if search_q := self.request.GET.get("q"):
            queryset = queryset.filter(title__icontains=search_q)
        if order_by := self.request.GET.get("order_by"):
            try:
                queryset = queryset.order_by(order_by)
            except FieldError:
                pass
        return queryset

    def get_context_data(self, **kwargs):
        """Add additional context (total item count ) to the context"""
        context = super().get_context_data(**kwargs)
        context["total_items"] = self.get_queryset().count()  # Total products count
        return context
    

class CustomerOrderDetailView(
    LoginRequiredMixin, HasCustomerAccessPermission, DetailView
):
    template_name = "dashboard/customer/orders/order-detail.html"


    def get_queryset(self):
        return OrderModel.objects.filter(user=self.request.user)
