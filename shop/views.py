import stripe
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from .models import Item, Order


def _get_stripe_keys(currency: str):
    """Return (public_key, secret_key) for the given currency."""
    if currency == 'eur':
        return settings.STRIPE_PUBLIC_KEY_EUR, settings.STRIPE_SECRET_KEY_EUR
    return settings.STRIPE_PUBLIC_KEY_USD, settings.STRIPE_SECRET_KEY_USD


# ── Item views ────────────────────────────────────────────────────────────────

def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    public_key, _ = _get_stripe_keys(item.currency)
    return render(request, 'shop/item.html', {
        'item': item,
        'stripe_public_key': public_key,
    })


def buy_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    public_key, secret_key = _get_stripe_keys(item.currency)
    stripe.api_key = secret_key

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': item.currency,
                'product_data': {'name': item.name},
                'unit_amount': item.stripe_price(),
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri('/') + 'success/',
        cancel_url=request.build_absolute_uri(f'/item/{pk}/'),
    )
    return JsonResponse({'id': session.id})


# ── Order views ───────────────────────────────────────────────────────────────

def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    currency = order.currency()
    public_key, _ = _get_stripe_keys(currency)
    return render(request, 'shop/order.html', {
        'order': order,
        'stripe_public_key': public_key,
    })


def buy_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    currency = order.currency()
    public_key, secret_key = _get_stripe_keys(currency)
    stripe.api_key = secret_key

    line_items = [
        {
            'price_data': {
                'currency': currency,
                'product_data': {'name': item.name},
                'unit_amount': item.stripe_price(),
            },
            'quantity': 1,
        }
        for item in order.items.all()
    ]

    kwargs = {
        'payment_method_types': ['card'],
        'line_items': line_items,
        'mode': 'payment',
        'success_url': request.build_absolute_uri('/') + 'success/',
        'cancel_url': request.build_absolute_uri(f'/order/{pk}/'),
    }

    # Attach discount (coupon) if present
    if order.discount and order.discount.stripe_coupon_id:
        kwargs['discounts'] = [{'coupon': order.discount.stripe_coupon_id}]

    # Attach tax rate to each line item if present
    if order.tax and order.tax.stripe_tax_rate_id:
        for li in kwargs['line_items']:
            li['tax_rates'] = [order.tax.stripe_tax_rate_id]

    session = stripe.checkout.Session.create(**kwargs)
    return JsonResponse({'id': session.id})


# ── Utility views ─────────────────────────────────────────────────────────────

def success(request):
    return render(request, 'shop/success.html')
