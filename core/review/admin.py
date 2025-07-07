from django.contrib import admin
from .models import ReviewModel


@admin.register(ReviewModel)
class ReviewModelAdmin(admin.ModelAdmin):
    """Admin configuration for ReviewModel"""

    list_display = ("id", "user", "product", 'rate', 'status', "created_date")