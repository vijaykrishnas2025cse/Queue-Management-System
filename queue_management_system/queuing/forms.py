from django import forms
from .models import QueueService

class QueueServiceForm(forms.ModelForm):
    """Form for creating and updating queue services."""
    class Meta:
        model = QueueService
        fields = ('service_name', 'service_type', 'description', 'estimated_service_time', 'is_active')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
