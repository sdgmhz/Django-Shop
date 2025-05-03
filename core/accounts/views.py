from django.contrib.auth import views as auth_views
from .forms import (
    CustomAuthenticationForm,
    CustomUserCreationForm,
    CustomPasswordResetForm,
    CustomSetPasswordForm,
)
from django.views import generic
from django.urls import reverse_lazy


class LoginView(auth_views.LoginView):
    """Login view using custom authentication form"""

    template_name = "accounts/login.html"
    form_class = CustomAuthenticationForm
    redirect_authenticated_user = True


class LogoutView(auth_views.LogoutView):
    """Logout view (inherits default behavior)"""

    pass


class RegisterView(generic.CreateView):
    """User registration view with custom user creation form"""

    form_class = CustomUserCreationForm
    template_name = "accounts/registration.html"
    success_url = reverse_lazy("website:index")


class PasswordResetView(auth_views.PasswordResetView):
    """Initiates password reset process by sending reset email"""

    email_template_name = "accounts/password_reset_email.html"
    form_class = CustomPasswordResetForm
    template_name = "accounts/password_reset_form.html"
    success_url = reverse_lazy("accounts:password_reset_done")


class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    """View shown after reset email is successfully sent"""

    template_name = "accounts/password_reset_done.html"


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    """View to confirm password reset and set new password"""

    form_class = CustomSetPasswordForm
    success_url = reverse_lazy("accounts:password_reset_complete")
    template_name = "accounts/password_reset_confirm.html"


class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    """Final view shown after password reset is complete"""

    template_name = "accounts/password_reset_complete.html"
