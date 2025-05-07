from django.contrib import admin

from .models import ContactModel, NewsletterModel


@admin.register(ContactModel)
class ContactModelAdmin(admin.ModelAdmin):
    """Admin configuration for ContactModel"""

    list_display = ["id", "email", "phone_number", "created_date"]
    list_filter = ["email", "phone_number"]
    empty_value_display = "Not provided"


@admin.register(NewsletterModel)
class NewsletterModelAdmin(admin.ModelAdmin):
    """Admin configuration for NewsletterModel"""

    list_display = ["id", "email", "created_date"]
