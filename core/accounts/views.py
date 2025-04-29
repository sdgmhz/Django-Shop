from django.contrib.auth import views as auth_views
from .forms import CustomAuthenticationForm, CustomUserCreationForm, CustomPasswordResetForm, CustomSetPasswordForm
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

class PasswordResetView(auth_views.PasswordResetView):
    email_template_name = "accounts/password_reset_email.html"
    form_class = CustomPasswordResetForm
    template_name = "accounts/password_reset_form.html"
    success_url = reverse_lazy("accounts:password_reset_done")

class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = "accounts/password_reset_done.html"

class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    form_class = CustomSetPasswordForm
    success_url = reverse_lazy("accounts:password_reset_complete")
    template_name = "accounts/password_reset_confirm.html"


class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = "accounts/password_reset_complete.html"



