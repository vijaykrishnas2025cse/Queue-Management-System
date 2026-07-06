# Template tags for user profiles
from django import template

register = template.Library()

@register.filter
def get_active_tokens(user):
    """Get count of active tokens for a user."""
    try:
        return user.tokens.filter(status__in=['waiting', 'ready']).count()
    except:
        return 0

@register.filter
def get_completed_tokens(user):
    """Get count of completed tokens for a user."""
    try:
        return user.tokens.filter(status='completed').count()
    except:
        return 0

@register.filter
def average_wait_time(user):
    """Calculate average wait time for a user."""
    try:
        total = 0
        count = 0
        for token in user.tokens.filter(status='completed'):
            wait_time = (token.updated_at - token.created_at).total_seconds() / 60
            total += wait_time
            count += 1
        
        if count == 0:
            return "0 min"
        
        avg = total / count
        return f"{int(avg)} min"
    except:
        return "0 min"
