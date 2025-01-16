from django.contrib import admin
from .models import Product, Category

# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'sku')
    fieldsets = (
        (None, {
            'fields': (
                'category', 'sku', 'name', 'short_description', 'description',
                'price', 'stock', 'rating', 'has_sizes'
            )
        }),
        ('Condition / Tag Info', {
            'fields': ('condition', 'tag_size', 'fabric_info', 'estimated_fit')
        }),
        ('Measurements', {
            'fields': ('shoulders', 'length', 'sleeve', 'armpit_to_armpit', 'waist', 'hips')
        }),
        ('Image', {
            'fields': ('image',)
        })
    )
    ordering = ('sku',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )