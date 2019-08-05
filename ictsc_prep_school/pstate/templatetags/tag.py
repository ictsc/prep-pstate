from django import template

from terraform_manager.models import Setting

register = template.Library()


@register.filter
def get_item(dictionary, key):
    return dictionary.getlist(key)


@register.simple_tag
def get_setting(key):
    try:
        #   FIX ME  :   Falseを返してもなぜかTrueになる.
        return Setting.objects.get(name=key)
    except:
        return ''
