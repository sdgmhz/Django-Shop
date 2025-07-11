from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from decimal import Decimal
from django.core.validators import MaxValueValidator, MinValueValidator


User = get_user_model()


class ProductStatusType(models.IntegerChoices):
    """Choices for product status (published or draft)"""

    published = 1, _("نمایش")
    draft = 2, _("عدم نمایش")


class ProductCategoryModel(models.Model):
    """Model representing product categories"""

    title = models.CharField(max_length=255)
    slug = models.SlugField(allow_unicode=True)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return the category title"""
        return self.title


class ProductModel(models.Model):
    """Model representing a product"""

    user = models.ForeignKey(User, on_delete=models.PROTECT)
    category = models.ManyToManyField(ProductCategoryModel)
    title = models.CharField(max_length=255)
    slug = models.SlugField(allow_unicode=True)
    image = models.ImageField(
        default="/default/product-image.png", upload_to="product/img/"
    )
    description = models.TextField()
    brief_description = models.TextField(null=True, blank=True)

    stock = models.PositiveIntegerField(default=0)
    price = models.DecimalField(default=0, max_digits=10, decimal_places=0)
    discount_percent = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    avg_rate = models.FloatField(default=0.0)

    status = models.IntegerField(
        choices=ProductStatusType.choices, default=ProductStatusType.draft.value
    )

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_date"]

    def __str__(self):
        """Return the product title"""
        return self.title

    def get_price(self):
        """Return the final price after applying discount"""
        return round(self.price * (1 - Decimal(self.discount_percent / 100)))

    def is_discounted(self):
        """Check if product has a discount"""
        return self.discount_percent != 0

    def is_published(self):
        return self.status == ProductStatusType.published.value


class ProductImageModel(models.Model):
    """Model representing extra images for a product"""

    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name="extra_image")
    file = models.ImageField(upload_to="product/extra-img/")

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)


class WishlistProductModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.title
