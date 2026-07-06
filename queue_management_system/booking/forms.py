from django import forms
from .models import Token

class BookTokenForm(forms.Form):
    """Form to book a token in a queue."""
    queue_id = forms.IntegerField(widget=forms.HiddenInput())
    
    class Meta:
        fields = ('queue_id',)
