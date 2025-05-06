import random
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from faker import Faker
from pathlib import Path
from django.core.files import File

from shop.models import ProductModel, ProductCategoryModel, ProductStatusType
from accounts.models import CustomUser, CustomUserType


BASE_DIR = Path(__file__).resolve().parent


class Command(BaseCommand):
    """Management command to generate fake product entries"""

    help = "Generate fake products"

    def __init__(self, *args, **kwargs):
        """Initialize the command and set up Faker"""
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker(locale="fa_IR")

    def handle(self, *args, **options):
        """Generate 10 fake product instances with random data"""
        user = CustomUser.objects.get(type=CustomUserType.admin.value)
        # List of images
        image_list = [
            "./images/img1.jpg",
            "./images/img2.jpg",
            "./images/img3.jpg",
            "./images/img4.jpg",
            "./images/img5.jpg",
            "./images/img6.jpg",
            "./images/img7.jpg",
            "./images/img8.jpg",
            # Add more image filenames as needed
        ]

        categories = ProductCategoryModel.objects.all()

        for _ in range(10):  # Generate 10 fake products
            user = user
            num_categories = random.randint(1, 4)
            selected_categories = random.sample(list(categories), num_categories)
            title = " ".join(self.fake.words(3))
            slug = slugify(title, allow_unicode=True)
            selected_image = random.choice(image_list)
            image_obj = File(
                file=open(BASE_DIR / selected_image, "rb"),
                name=Path(selected_image).name,
            )
            description = self.fake.paragraph(nb_sentences=10)
            brief_description = self.fake.paragraph(nb_sentences=1)
            stock = self.fake.random_int(min=0, max=10)
            status = random.choice(ProductStatusType.choices)[0]
            price = self.fake.random_int(min=10000, max=100000)
            discount_percent = self.fake.random_int(min=0, max=50)

            product = ProductModel.objects.create(
                user=user,
                title=title,
                slug=slug,
                image=image_obj,
                description=description,
                brief_description=brief_description,
                stock=stock,
                status=status,
                price=price,
                discount_percent=discount_percent,
            )
            product.category.set(selected_categories)

        self.stdout.write(self.style.SUCCESS("Successfully generated 10 fake products"))
