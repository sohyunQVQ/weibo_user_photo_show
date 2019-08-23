from django import template
import random

register = template.Library()

@register.simple_tag
def number():
    return random.randint(1,4)