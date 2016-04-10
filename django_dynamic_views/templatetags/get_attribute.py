import re
from django.conf import settings
from django.template.defaulttags import register
from django.utils.safestring import mark_safe


@register.filter
def get_attribute_recursive(value, arg, return_as_string=True):
    """
    Gets an attribute of an object dynamically from a string name
    """
    if arg is None:
        return mark_safe("")

    if '__' in arg:
        arg_list = arg.split('__')
    elif '.' in arg:
        arg_list = arg.split('.')
    else:
        arg_list = [arg]

    for arg in arg_list:
        value = get_attribute(value, arg, return_as_string=False)

    if return_as_string:
        value = mark_safe(value)

    return value


@register.filter
def get_attribute(value, arg, return_as_string=True):
    """
    Gets an attribute of an object dynamically from a string name
    """
    numeric_test = re.compile("^\d+$")

    if hasattr(value, '__iter__') and arg in value:
        value = value[arg]
    elif hasattr(value, str(arg)):
        value = getattr(value, arg)
    elif numeric_test.match(str(arg)) and len(value) > int(arg):
        value = value[int(arg)]
    else:
        return settings.TEMPLATE_STRING_IF_INVALID

    if hasattr(value, '__call__'):
        value = value()

    if return_as_string:
        value = mark_safe(value)

    return value
