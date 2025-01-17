from django.shortcuts import render
from .models import HeroImage


def index(request):
    """ A view to display the index page """
    
    return render(request, 'home/index.html')

def index(request):
    hero_images = HeroImage.objects.filter(is_active=True)
    return render(request, 'home/index.html', {'hero_images': hero_images})


def about_page(request):
    return render(request, 'about.html')