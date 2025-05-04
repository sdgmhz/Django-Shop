from django.core.management.base import BaseCommand
from faker import Faker
from django.utils.text import slugify

from shop.models import ProductCategoryModel


class Command(BaseCommand):
    help = "Generate fake categories"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker()

    def handle(self, *args, **options):
        for _ in range(10):
            title = " ".join(self.fake.words(2))
            slug = slugify(title, allow_unicode=True)
            ProductCategoryModel.objects.get_or_create(title=title, slug=slug)

        self.stdout.write(
            self.style.SUCCESS("Successfully generated 10 fake categories")
        )
