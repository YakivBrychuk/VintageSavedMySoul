from django.shortcuts import (
    render, redirect, reverse, HttpResponse, get_object_or_404
)
from django.contrib import messages

from products.models import Product


def view_bag(request):
    """ A view that renders the bag contents page """

    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

    product = get_object_or_404(Product, pk=item_id)
    quantity_requested = int(request.POST.get('quantity', 1))
    redirect_url = request.POST.get('redirect_url', 'products')
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    bag = request.session.get('bag', {})

    # Check stock availability
    if quantity_requested > product.stock:
        quantity_requested = product.stock  # Clamp to available stock
        messages.warning(request, f"We only have {product.stock} in stock for {product.name}. Adjusted quantity.")
    elif product.stock == 0:
        messages.error(request, f"{product.name} is out of stock.")
        return redirect(redirect_url)

    if size:
        if item_id in list(bag.keys()):
            if size in bag[item_id]['items_by_size']:
                # Add to existing size quantity, but don't exceed stock
                new_quantity = bag[item_id]['items_by_size'][size] + quantity_requested
                if new_quantity > product.stock:
                    new_quantity = product.stock
                    messages.warning(request, f"Quantity for size {size.upper()} {product.name} adjusted to stock limit.")
                bag[item_id]['items_by_size'][size] = new_quantity
                messages.success(request,
                                 (f'Updated size {size.upper()} '
                                  f'{product.name} quantity to '
                                  f'{bag[item_id]["items_by_size"][size]}'))
            else:
                bag[item_id]['items_by_size'][size] = quantity_requested
                messages.success(request,
                                 (f'Added size {size.upper()} '
                                  f'{product.name} to your bag'))
        else:
            bag[item_id] = {'items_by_size': {size: quantity_requested}}
            messages.success(request,
                             (f'Added size {size.upper()} '
                              f'{product.name} to your bag'))
    else:
        if item_id in list(bag.keys()):
            # Add to existing quantity, but don't exceed stock
            new_quantity = bag[item_id] + quantity_requested
            if new_quantity > product.stock:
                new_quantity = product.stock
                messages.warning(request, f"Quantity for {product.name} adjusted to stock limit.")
            bag[item_id] = new_quantity
            messages.success(request,
                             (f'Updated {product.name} '
                              f'quantity to {bag[item_id]}'))
        else:
            bag[item_id] = quantity_requested
            messages.success(request, f'Added {product.name} to your bag')

    request.session['bag'] = bag
    return redirect(redirect_url)


def adjust_bag(request, item_id):
    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    size = request.POST.get('product_size', None)
    bag = request.session.get('bag', {})

    # If they request more than in stock, clamp it
    if quantity > product.stock:
        quantity = product.stock
        adjustment_message = f"We only have {product.stock} in stock for {product.name}. Adjusted quantity to {quantity}."
    elif product.stock == 0:
        messages.error(request, f"{product.name} is out of stock.")
        # Remove item from bag
        if size:
            bag[item_id]['items_by_size'].pop(size, None)
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id, None)
        else:
            bag.pop(item_id, None)
        request.session['bag'] = bag
        return redirect(reverse('view_bag'))
    else:
        adjustment_message = None

    # Then proceed
    if size:
        if quantity > 0:
            bag[item_id]['items_by_size'][size] = quantity
            if adjustment_message:
                messages.success(request, f"{adjustment_message} Updated size {size.upper()} {product.name} to {quantity}")
            else:
                messages.success(request, f'Updated size {size.upper()} {product.name} to {quantity}')
        else:
            # remove that size
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id, None)
            messages.success(request, f'Removed size {size.upper()} {product.name} from your bag')
    else:
        if quantity > 0:
            bag[item_id] = quantity
            if adjustment_message:
                messages.success(request, f"{adjustment_message} Updated {product.name} quantity to {quantity}")
            else:
                messages.success(request, f'Updated {product.name} quantity to {quantity}')
        else:
            bag.pop(item_id, None)
            messages.success(request, f'Removed {product.name} from your bag')

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))
def remove_from_bag(request, item_id):
    """Remove the item from the shopping bag"""

    try:
        product = get_object_or_404(Product, pk=item_id)
        size = None
        if 'product_size' in request.POST:
            size = request.POST['product_size']
        bag = request.session.get('bag', {})

        if size:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
            messages.success(request,
                             (f'Removed size {size.upper()} '
                              f'{product.name} from your bag'))
        else:
            bag.pop(item_id)
            messages.success(request, f'Removed {product.name} from your bag')

        request.session['bag'] = bag
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)