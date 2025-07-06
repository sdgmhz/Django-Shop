from django.db import models
from shop.models import ProductModel
from django.core.validators import MinValueValidator, MaxValueValidator
from django.dispatch import receiver
from django.db.models.signals import post_save


class ReviewStatusType(models.IntegerChoices):
    pending = 1, "در انتظار تأیید"
    accepted = 2, "تأیید شده"
    rejected = 3, "رد شده"


class ReviewModel(models.Model):
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name="product_reviews")
    description = models.TextField()
    rate = models.IntegerField(default=5, validators=[MinValueValidator(0), MaxValueValidator(5)])
    status = models.IntegerField(choices=ReviewStatusType.choices, default=ReviewStatusType.pending.value)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_date"]

    def __str__(self):
        return f"{self.user}-{self.product.title}"

@receiver(post_save, sender=ReviewModel)
def calculate_avf_review(sender, instance, created, **kwargs):
    pass