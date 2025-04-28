from django.core.management.base import BaseCommand
from shop.models import Product, Category  # Change 'shop' to your app name
from PIL import Image

class Command(BaseCommand):
    help = "Resize all existing images to a fixed size"

    def handle(self, *args, **kwargs):
        max_product_size = (500, 500)
        max_category_size = (400, 400)

        for product in Product.objects.all():
            if product.product_image:
                img_path = product.product_image.path
                img = Image.open(img_path)
                img.thumbnail(max_product_size)
                img.save(img_path)

        for category in Category.objects.all():
            if category.image:
                img_path = category.image.path
                img = Image.open(img_path)
                img.thumbnail(max_category_size)
                img.save(img_path)

        self.stdout.write(self.style.SUCCESS("✅ All images resized successfully!"))
