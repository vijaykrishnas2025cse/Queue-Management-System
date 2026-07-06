from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class QueueService(models.Model):
    SERVICE_CHOICES = [
        ('hospital', 'Hospital'),
        ('juice_shop', 'Juice Shop'),
        ('voting_booth', 'Voting Booth'),
        ('bank', 'Bank'),
        ('clinic', 'Clinic'),
        ('other', 'Other Service'),
    ]
    
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='managed_queues')
    service_name = models.CharField(max_length=100)
    service_type = models.CharField(max_length=20, choices=SERVICE_CHOICES, default='other')
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    estimated_service_time = models.IntegerField(default=5, help_text="Time in minutes per token")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.service_name} (#{self.id})"

    def get_current_token_count(self):
        """Get total number of tokens in this queue"""
        from booking.models import Token
        return Token.objects.filter(queue=self, status__in=['waiting', 'ready']).count()

    def get_next_token(self):
        """Get the next token to be served"""
        from booking.models import Token
        return Token.objects.filter(queue=self, status='waiting').order_by('token_number').first()

    class Meta:
        verbose_name_plural = "Queue Services"
