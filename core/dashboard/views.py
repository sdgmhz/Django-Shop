from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from accounts.models import CustomUserType

class DashboardHomeView(LoginRequiredMixin, View):
    
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.type == CustomUserType.customer.value:
                return redirect(reverse_lazy('dashboard:customer:home'))
            if request.user.type == CustomUserType.admin.value:
                return redirect(reverse_lazy('dashboard:admin:home'))
        else:
            return redirect(reverse_lazy("accounts:login"))
        return super().dispatch(request, *args, **kwargs)