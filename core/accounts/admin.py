from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

from .models import Profile

UserModel = get_user_model()


@admin.register(UserModel)
class CustomUserAdmin(UserAdmin):
    """Custom admin panel configuration for the CustomUser model."""
    model = UserModel
    list_display = ("id", "email", "is_superuser", "is_active", "is_verified")
    list_filter = ("email", "is_superuser", "is_active", "is_verified")
    search_fields = ("email",)
    ordering = ("created_date",)
    fieldsets = (
        # Section: authentication credentials
        ("Authentication", {"fields": ("email", "password")}),
        # Section: user permission flags
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "is_verified",
                )
            },
        ),
        # Section: group and permission assignment
        (
            "group permissions",
            {
                "fields": (
                    "groups",
                    "user_permissions",
                    "type",
                )
            },
        ),
        # Section: metadata
        ("Important date", {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        # Section: fields for user creation form
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "is_verified",
                    "type",
                ),
            },
        ),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Admin configuration for the Profile model."""
    list_display = ("id", "user", "first_name", "last_name", "phone_number")
    searching_fields = ("user", "first_name", "last_name", "phone_number")

