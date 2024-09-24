import os
import subprocess
from django.core.exceptions import ValidationError
from django.db import models
from PIL import Image
from pillow_avif import AvifImagePlugin

def validate_image_extension(value):
    ext = value.name.split('.')[-1].lower()
    valid_extensions = ['jpg', 'jpeg', 'png', 'avif', 'webp']
    if ext not in valid_extensions:
        raise ValidationError(f'Unsupported file extension: {ext}. Supported formats: jpg, jpeg, png, avif, webp.')

class HeroImage(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='hero_images/', validators=[validate_image_extension])
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title or "Hero Image"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Check if image needs to be converted to AVIF
        if self.image and self.image.path.endswith(('.jpg', '.jpeg', '.png', '.webp')):
            self.convert_to_avif()

    def convert_to_avif(self):
        """Converts the current image to AVIF format."""
        avif_image_path = self.image.path.rsplit('.', 1)[0] + '.avif'

        try:
            # Run the AVIF conversion using avifenc
            subprocess.run(['avifenc', self.image.path, avif_image_path], check=True)

            # Remove the original image file after conversion
            if os.path.exists(self.image.path):
                os.remove(self.image.path)

            # Update the image field to point to the AVIF file
            self.image.name = f'hero_images/{os.path.basename(avif_image_path)}'
            super().save()  # Save to update the image path

        except subprocess.CalledProcessError as e:
            print(f"Error converting to AVIF: {e}")

    @property
    def image_url(self):
        """Return the URL of the image if it exists."""
        if self.image:
            return self.image.url
        return None
