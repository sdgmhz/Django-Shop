from django import forms
from .models import ContactModel, NewsletterModel
from captcha.fields import CaptchaField


class ContactModelForm(forms.ModelForm):
    """Form for submitting contact messages."""

    captcha = CaptchaField()

    class Meta:
        """Meta options for ContactModelForm."""

        model = ContactModel
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "captcha",
            "message",
        ]


class NewsletterForm(forms.ModelForm):
    """Form for subscribing to the newsletter."""

    class Meta:
        """Meta options for NewsletterForm."""

        model = NewsletterModel
        fields = ("email",)
