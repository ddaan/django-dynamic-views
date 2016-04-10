from django.conf import settings
from django.template.defaulttags import register

from .get_attribute import get_attribute_recursive


@register.simple_tag()
def field_value(object, field_name, convert_field_values, view, *args, **kwargs):
    """
    Retrieves field name from the object and converts its value

    :param object: object in the field set
    :param field_name: field name (e.g. comment__author )
    :param convert_field_values: mapping of methods to be called on the view class
    :param view: view class
    :param args:
    :param kwargs:
    :return: string value
    """
    value = get_attribute_recursive(object, field_name, return_as_string=False)
    if convert_field_values.get(field_name):
        try:
            value = getattr(view, convert_field_values.get(field_name))(value)
        except Exception as e:
            if settings.DEBUG:
                value = 'Error parsing {}: {}'.format(convert_field_values.get(field_name, str(e)))
            else:
                value = ''

    return value
