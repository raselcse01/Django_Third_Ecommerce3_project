from django import template
import math

register = template.Library()

@register.simple_tag
def call_sellprice(Price, Discount):
    if Discount is None or Discount is 0:
        return Price
    sellprice = Price
    sellprice = Price - (Price * Discount/100)
    return math.floor(sellprice)

@register.simple_tag
def progress_bar(Total_quantity, Availability):

    progress_bar = Availability
    progress_bar = Availability * (100/Total_quantity)
    return math.floor(progress_bar)