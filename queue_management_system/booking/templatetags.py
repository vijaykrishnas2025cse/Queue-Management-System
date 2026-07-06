# Filters for template tags
from django import template

register = template.Library()

@register.filter
def status_color(status):
    """Return Bootstrap color class for status."""
    colors = {
        'waiting': 'warning',
        'ready': 'info',
        'serving': 'danger',
        'completed': 'success',
        'cancelled': 'secondary',
    }
    return colors.get(status, 'secondary')

@register.filter
def filter_by_status(tokens, status):
    """Filter tokens by status."""
    return [t for t in tokens if t.status == status]
