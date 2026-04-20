from django.contrib import admin
from .models import Item, Order, Discount, Tax


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'currency')
    search_fields = ('name',)
    list_filter = ('currency',)


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('name', 'stripe_coupon_id', 'percent_off', 'amount_off')


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ('name', 'stripe_tax_rate_id', 'percentage', 'inclusive')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_total_price', 'discount', 'tax', 'created_at')

    def get_total_price(self, obj):
        return obj.total_price()
    get_total_price.short_description = 'Total Price'
