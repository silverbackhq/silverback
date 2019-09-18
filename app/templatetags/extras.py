"""
    Template Extra Tags
    ~~~~~~~~~~~~~~

    {% load extras %}
    {{ somevariable|cut:"0" }}

    :copyright: silverbackhq
    :license: BSD-3-Clause
"""

# Third Party Library
from django import template


register = template.Library()


@register.filter(name='cut')
def cut(value, arg):
    """Removes all values of arg from the given string"""
    return value.replace(arg, '')
