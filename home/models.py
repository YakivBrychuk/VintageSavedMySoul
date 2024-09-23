from django.db import models

class HeroImage(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='hero_images/')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title or "Hero Image"
