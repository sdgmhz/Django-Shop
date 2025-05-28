from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .permissions import HasCustomerAccessPermission


class OrderCheckOutView(LoginRequiredMixin, HasCustomerAccessPermission, TemplateView):
    template_name = "order/checkout.html"