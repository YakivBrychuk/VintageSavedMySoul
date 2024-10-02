from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
from bag.contexts import bag_contents

import stripe

def checkout(request):
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse('products'))

    current_bag = bag_contents(request)
    total_bag = current_bag['total_bag']
    stripe_total = round(total_bag * 100)

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51Q5RXdP0IWaG1xGQEYf2X3kgDu3JXdBc4GP8gZsMYgvebHB8R29UFtx6vcrQdH6P2OItOLt8uupHKFmDkj4K3uU5001o7emsi3',
        'client_secret': 'test client secret'
    }


    return render(request, template, context)