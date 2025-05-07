from django.contrib import admin

from .models import ContactModel, NewsletterModel


@admin.register(ContactModel)
class ContactModelAdmin(admin.ModelAdmin):
    list_display = ["id", "email", "phone_number", "created_date"]
    empty_value_display = "Not provided"
