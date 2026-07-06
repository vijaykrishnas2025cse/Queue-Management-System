# Template tags for token filtering
from django import template

register = template.Library()

@register.filter
def filter_by_status(tokens, status):
    """Filter tokens by status."""
    try:
        return [t for t in tokens if t.status == status]
    except:
        return []

@register.filter
def active_count(tokens):
    """Count active tokens."""
    try:
        return len([t for t in tokens if t.status in ['waiting', 'ready']])
    except:
        return 0
