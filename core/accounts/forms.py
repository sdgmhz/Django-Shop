from django.contrib.auth import forms as auth_forms
from captcha.fields import CaptchaField
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomAuthenticationForm(auth_forms.AuthenticationForm):
    """Custom authentication form with captcha."""

    captcha = CaptchaField()

    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)

        # if not user.is_verified:
        #     raise ValidationError("user is not verified")
        
    # class Meta:
    #     model = User
    #     fields = ('username', 'password', 'captcha')


class CustomUserCreationForm(auth_forms.UserCreationForm):
    """Custom user creation form with captcha."""

    captcha = CaptchaField()

    class Meta:
        model = User
        fields = ("email", "password1", "password2", "captcha")
    
