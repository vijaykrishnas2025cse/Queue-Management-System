# Template tags for status colors and filtering
from django import template
from booking.models import Token

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
def multiply(value, arg):
    """Multiply the value by the argument."""
    try:
        return int(value) * int(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def add(value, arg):
    """Add the value and argument."""
    try:
        return int(value) + int(arg)
    except (ValueError, TypeError):
        return value

@register.simple_tag
def user_tokens_active(user):
    """Get count of user's active tokens."""
    return Token.objects.filter(
        user=user,
        status__in=['waiting', 'ready', 'serving']
    ).count()

@register.simple_tag
def user_tokens_completed(user):
    """Get count of user's completed tokens."""
    return Token.objects.filter(
        user=user,
        status='completed'
    ).count()

@register.simple_tag
def user_tokens_average_wait(user):
    """Get average wait time for user's completed tokens."""
    completed_tokens = Token.objects.filter(
        user=user,
        status='completed'
    )
    if completed_tokens.exists():
        total_wait = sum(token.get_tokens_ahead() * token.queue.estimated_service_time for token in completed_tokens)
        return f"{total_wait // completed_tokens.count()} min"
    return "0 min"
