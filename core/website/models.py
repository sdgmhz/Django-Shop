from django.db import models

from .validators import validate_persian_name, validate_iranian_mobile


class ContactModel(models.Model):
    """Model for storing contact form submissions."""

    first_name = models.CharField(max_length=255, validators=[validate_persian_name])
    last_name = models.CharField(max_length=255, validators=[validate_persian_name])
    email = models.EmailField()
    phone_number = models.CharField(
        max_length=14, blank=True, null=True, validators=[validate_iranian_mobile]
    )
    message = models.TextField()

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta options for ContactModel."""

        ordering = ("-created_date",)

    def __str__(self):
        """Return email as string representation."""
        return self.email


class NewsletterModel(models.Model):
    """Model for storing newsletter subscription emails."""

    email = models.EmailField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return email as string representation."""
        return self.email
