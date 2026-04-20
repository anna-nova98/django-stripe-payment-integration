from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


CURRENCY_CHOICES = [
    ('usd', 'USD'),
    ('eur', 'EUR'),
]


class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='usd')

    def __str__(self):
        return f'{self.name} ({self.price} {self.currency.upper()})'

    def stripe_price(self):
        """Return price in cents (Stripe expects integer)."""
        return int(self.price * 100)


class Discount(models.Model):
    name = models.CharField(max_length=255)
    stripe_coupon_id = models.CharField(max_length=255, help_text='Stripe Coupon ID')
    percent_off = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        validators=[MinValueValidator(Decimal('0'))]
    )
    amount_off = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True,
        validators=[MinValueValidator(Decimal('0'))]
    )

    def __str__(self):
        return self.name


class Tax(models.Model):
    name = models.CharField(max_length=255)
    stripe_tax_rate_id = models.CharField(max_length=255, help_text='Stripe Tax Rate ID')
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    inclusive = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name} ({self.percentage}%)'


class Order(models.Model):
    items = models.ManyToManyField(Item, related_name='orders')
    discount = models.ForeignKey(
        Discount, null=True, blank=True, on_delete=models.SET_NULL
    )
    tax = models.ForeignKey(
        Tax, null=True, blank=True, on_delete=models.SET_NULL
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order #{self.pk} ({self.created_at.strftime("%Y-%m-%d")})'

    def total_price(self):
        return sum(item.price for item in self.items.all())

    def currency(self):
        """All items in an order must share the same currency."""
        currencies = self.items.values_list('currency', flat=True).distinct()
        if currencies.count() == 1:
            return currencies.first()
        return 'usd'  # fallback
