from django.contrib.auth import views as auth_views
from .forms import CustomAuthenticationForm, CustomUserCreationForm
from django.views import generic
from django.urls import reverse_lazy



class LoginView(auth_views.LoginView):
    template_name = 'accounts/login.html'
    form_class = CustomAuthenticationForm
    redirect_authenticated_user = True

class LogoutView(auth_views.LogoutView):
    pass


class RegisterView(generic.CreateView):
    form_class = CustomUserCreationForm
    template_name = 'accounts/registration.html'
    success_url = reverse_lazy("website:index")