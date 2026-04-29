from django import template
from decimal import Decimal

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def add_vat(amount, vat_pct):
    try:
        amt = Decimal(amount)
        vat = Decimal(vat_pct or '15')
        return str((amt * (1 + vat/100)).quantize(Decimal('0.01')))
    except Exception:
        return amount
