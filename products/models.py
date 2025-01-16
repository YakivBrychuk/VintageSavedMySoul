from django.contrib.auth.models import User
import os
import subprocess
from django.core.exceptions import ValidationError
from django.db import models
from pillow_avif import AvifImagePlugin
from PIL import Image


class Category(models.Model):
    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


def validate_image_extension(value):
    ext = value.name.split('.')[-1].lower()
    valid_extensions = ['jpg', 'jpeg', 'png', 'avif', 'webp']
    if ext not in valid_extensions:
        raise ValidationError(f'Unsupported file extension: {ext}. Supported formats: jpg, jpeg, png, avif, webp.')


class Product(models.Model):
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    has_sizes = models.BooleanField(default=False, null=True, blank=True)  # size
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='images/', validators=[validate_image_extension])
    # Many-to-Many relationship with User model for favoriting products
    favorited_by = models.ManyToManyField(
        User, related_name='favorite_products', blank=True
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Save the model first to ensure the image is available
        super().save(*args, **kwargs)

        if self.image and hasattr(self.image, 'path'):  # Ensure an image exists and has a file path
            # Perform the image processing
            try:
                image_path = self.image.path
                if image_path.endswith('.webp'):
                    with Image.open(image_path) as img:
                        # Convert WebP to PNG
                        png_image_path = image_path.rsplit('.', 1)[0] + '.png'
                        img.save(png_image_path, 'PNG')

                    # Update the image path to PNG
                    self.image.name = f'images/{os.path.basename(png_image_path)}'
                    self.save(update_fields=['image'])

                # Convert JPEG/PNG to AVIF
                if image_path.endswith(('.jpg', '.jpeg', '.png')):
                    avif_image_path = image_path.rsplit('.', 1)[0] + '.avif'
                    subprocess.run(['avifenc', image_path, avif_image_path], check=True)

                    # Remove the original image after conversion
                    if os.path.exists(image_path):
                        os.remove(image_path)

                    # Update the image path to the AVIF version
                    self.image.name = f'images/{os.path.basename(avif_image_path)}'
                    self.save(update_fields=['image'])

            except subprocess.CalledProcessError as e:
                print(f"Error converting to AVIF: {e}")
            except Exception as e:
                print(f"Error processing image: {e}")

    # Dynamic URL access for images
    @property
    def image_url(self):
        if self.image:
            return self.image.url
        return None
