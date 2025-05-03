from django.contrib import admin
from .models import ProductModel, ProductImageModel, ProductCategoryModel

@admin.register(ProductModel)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "stock", "status", "created_date",)

@admin.register(ProductCategoryModel)
class ProductCategoryModelAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "created_date",)

@admin.register(ProductImageModel)
class ProductImageModel(admin.ModelAdmin):
    list_display = ("id", "file", "created_date")