from django.shortcuts import render
from .models import HeroImage
# Create your views here.

def index(request):
    """ A view to display the index page """
    
    return render(request, 'home/index.html')

def home(request):
    hero_images = HeroImage.objects.filter(is_active=True)
    return render(request, 'home/index.html', {'hero_images': hero_images})