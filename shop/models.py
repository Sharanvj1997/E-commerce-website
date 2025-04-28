from django.db import models
import datetime
import os
from PIL import Image 
from django.contrib.auth.models import User # Import Pillow for image processing

# Function to generate unique filenames
def getFileName(request, filename):
    now_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")  # Remove colons
    new_filename = f"{now_time}_{filename}"
    return os.path.join('uploads/', new_filename)

class Category(models.Model):
    name = models.CharField(max_length=150, null=False, blank=False)
    image = models.ImageField(upload_to=getFileName, null=True, blank=True)
    description = models.TextField(max_length=500, null=False, blank=False)
    status = models.BooleanField(default=False, help_text="0-show,1-Hidden")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the original image first
        if self.image:
            img = Image.open(self.image.path)
            max_size = (400, 400)  # Resize to a max of 400x400 pixels
            img.thumbnail(max_size)  # Maintain aspect ratio
            img.save(self.image.path)  # Overwrite the original image


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, null=False, blank=False)
    vendor = models.CharField(max_length=150, null=False, blank=False)
    product_image = models.ImageField(upload_to=getFileName, null=True, blank=True)
    quantity = models.IntegerField(null=False, blank=False)
    original_price = models.FloatField(null=False, blank=False)
    selling_price = models.FloatField(null=False, blank=False)
    description = models.TextField(max_length=500, null=False, blank=False)
    status = models.BooleanField(default=False, help_text="0-show,1-Hidden")
    trending = models.BooleanField(default=False, help_text="0-default,1-Trending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the original image first
        if self.product_image:
            img = Image.open(self.product_image.path)
            max_size = (500, 500)  # Resize to a max of 500x500 pixels
            img.thumbnail(max_size)  # Maintain aspect ratio
            img.save(self.product_image.path)  # Overwrite the original image
