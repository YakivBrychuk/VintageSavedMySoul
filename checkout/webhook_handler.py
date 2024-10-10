from django.http import HttpResponse



class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request


    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """
        intent = event.data.object
        pid = intent.id
        bag = intent.metadata.bag
        save_info = intent.metadata.save_info

        billing_details = intent.charges.data[0].billing_details
        shipping_details = intent.shipping
        grand_total = round(intent.charges.data[0].amount / 100, 2)

        # Clean data in the shipping details
        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None

        order_exists = False
        try:
            order = order.objects.get (
                full_name__iexact=billing_details.name,
                email__iexact=billing_details.email,
                phone_number__iexact=billing_details.phone,
                country__iexact=billing_details.address.country,
                postcode__iexact=billing_details.address.postal_code,
                town_or_city__iexact=billing_details.address.city,
                street_address1__iexact=billing_details.address.line1,
                street_address2__iexact=billing_details.address.line2,
                county__iexact=billing_details.address.state,
                grand_total=grand_total,
                original_bag=bag,
                stripe_pid=pid,
            )
            order_exists = True
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS:Verified order already in database',
                status=200) 
        except order.DoesNotExist:
            for item_id, item_data in json.loads(bag).items():
                order = Order.objects.create(
                    full_name__iexact=billing_details.name,
                    email__iexact=billing_details.email,
                    phone_number__iexact=billing_details.phone,
                    country__iexact=billing_details.address.country,
                    postcode__iexact=billing_details.address.postal_code,
                    town_or_city__iexact=billing_details.address.city,
                    street_address1__iexact=billing_details.address.line1,
                    street_address2__iexact=billing_details.address.line2,
                    county__iexact=billing_details.address.state,
                )
                product = Product.objects.get(id=item_id)
                if isinstance(item_data, int):
                    order_line_item = OrderLineItem(
                        order=order,
                        product=product,
                        quantity=item_data,
                    )
                    order_line_item.save()
                else:
                    for size, quantity in item_data['items_by_size'].items():
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            quantity=quantity,
                            product_size=size,
                        )
                        order_line_item.save()

        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)