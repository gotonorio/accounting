from django import template

register = template.Library()


@register.simple_tag
def url_replace(request, field, value):
    """GETパラメータを一部を置き換える."""
    url_dict = request.GET.copy()
    url_dict[field] = str(value)
    return url_dict.urlencode()


@register.filter
def subtract(value, arg):
    """ 引き算用フィルタ """
    if value:
        ret = value-arg
    else:
        ret = 0
    return ret


@register.filter
def div(value, arg):
    """ 割り算用フィルタ """
    if arg == 0:
        return ''
    return value // arg


@register.filter
def multi(value, arg):
    """ 掛け算. """
    return int(value*arg)