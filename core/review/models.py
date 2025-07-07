from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models import Avg

from shop.models import ProductModel


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
    
    def get_status(self):
        return {
            "id":self.status,
            "title":ReviewStatusType(self.status).name,
            "label":ReviewStatusType(self.status).label,
        }
        

@receiver(post_save, sender=ReviewModel)
def calculate_avf_review(sender, instance, created, **kwargs):
    if instance.status == ReviewStatusType.accepted.value:
        product = instance.product
        average_rating = ReviewModel.objects.filter(product=product, status=ReviewStatusType.accepted).aggregate(Avg('rate'))['rate__avg']
        product.avg_rate = round(average_rating,1)
        product.save()