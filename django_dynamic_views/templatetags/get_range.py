from django.template import Library

register = Library()


@register.filter
def get_range(value):
    """
    Filter - returns a list containing range made from given value.
    The range starts at 1 and stops at value.
    Usage (in template):

    <ul>{% for i in 3|get_range %}
      <li>{{ i }}. Do something</li>
    {% endfor %}</ul>

    Results with the HTML:
    <ul>
      <li>1. Do something</li>
      <li>2. Do something</li>
      <li>3. Do something</li>
    </ul>

    Instead of 3 one may use the variable set in the views
    """
    return range(value)
