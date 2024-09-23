from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages 
from django.db.models import Q
from .models import Product, Category

def all_products(request):
    """ A view to display all products, including sorting and search queries """

    products = Product.objects.all()
    query = None
    categories = None  # Initialize categories variable

    if request.GET:
        # Handle category filtering
        if 'category' in request.GET:
            # Split the category query param into a list
            categories = request.GET['category'].split(',')
            
            # First retrieve matching Category objects, then filter products by these categories
            category_objects = Category.objects.filter(name__in=categories)

            if category_objects.exists():
                products = products.filter(category__in=category_objects)
            else:
                messages.error(request, "No matching categories found!")

        # Handle search query
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))

            # Apply search filtering
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    context = {
        'products': products,
        'search_term': query,
        'selected_categories': categories,  # Pass categories to context
    }

    return render(request, 'products/products.html', context)



def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)
    
    # Ensure 'query' and 'categories' are properly handled
    query = request.GET.get('q', None)  # Default to None if not present
    categories = request.GET.get('category', None)  # Default to None if not present

    context = {
        'product': product,
        'search_term': query,
        'current_categories': categories.split(',') if categories else None,  # If categories exist, split them
    }

    return render(request, 'products/product_detail.html', context)
