from django.contrib.auth import forms as auth_forms
from captcha.fields import CaptchaField
from django.contrib.auth import get_user_model
from .tasks import send_reset_email_task


User = get_user_model()


class CustomAuthenticationForm(auth_forms.AuthenticationForm):
    """Custom authentication form with captcha."""

    captcha = CaptchaField()

    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)

        # if not user.is_verified:
        #     raise ValidationError("user is not verified")

    class Meta:
        model = User
        fields = ("email", "password")


class CustomUserCreationForm(auth_forms.UserCreationForm):
    """Custom user creation form with captcha."""

    captcha = CaptchaField()

    class Meta:
        model = User
        fields = ("email", "password1", "password2")


class CustomPasswordResetForm(auth_forms.PasswordResetForm):
    """Custom password reset form with captcha."""

    captcha = CaptchaField()

    def send_mail(
        self,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name=None,
    ):
        """Override send_mail to use Celery for sending email asynchronously"""

        safe_context = {
            "email": context.get("email"),
            "domain": context.get("domain"),
            "site_name": context.get("site_name"),
            "uid": context.get("uid"),
            "user": context.get("user").pk,
            "token": context.get("token"),
            "protocol": context.get("protocol"),
        }

        send_reset_email_task.delay(
            subject_template_name,
            email_template_name,
            safe_context,
            from_email,
            to_email,
            html_email_template_name,
        )

    class Meta:
        model = User
        fields = ("email",)


class CustomSetPasswordForm(auth_forms.SetPasswordForm):
    """Custom set password form with captcha."""

    captcha = CaptchaField()

    class Meta:
        model = User
        fields = ("new_password1", "new_password2")
