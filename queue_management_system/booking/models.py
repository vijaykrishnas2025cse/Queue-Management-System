from django.db import models
from django.contrib.auth.models import User
from queuing.models import QueueService
import qrcode
from io import BytesIO
from django.core.files import File
import uuid

class Token(models.Model):
    STATUS_CHOICES = [
        ('waiting', 'Waiting'),
        ('ready', 'Ready'),
        ('serving', 'Serving'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    queue = models.ForeignKey(QueueService, on_delete=models.CASCADE, related_name='tokens')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tokens')
    token_number = models.IntegerField()
    unique_id = models.CharField(max_length=50, unique=True, default=uuid.uuid4)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='waiting')
    qr_code = models.ImageField(upload_to='qr_codes/', null=True, blank=True)
    notification_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Token #{self.token_number} - Queue: {self.queue.service_name}"

    def generate_qr_code(self):
        """Generate QR code for the token."""
        qr_data = f"{self.unique_id}|{self.token_number}|{self.queue.id}"
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(qr_data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save to file
        img_io = BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)
        
        self.qr_code.save(f'qr_{self.unique_id}.png', File(img_io), save=False)

    def save(self, *args, **kwargs):
        if not self.pk:  # Only generate QR on creation
            super().save(*args, **kwargs)
            self.generate_qr_code()
        super().save(*args, **kwargs)

    def get_position_in_queue(self):
        """Get the current position of this token in the queue."""
        return Token.objects.filter(
            queue=self.queue,
            token_number__lt=self.token_number,
            status__in=['waiting', 'ready', 'serving']
        ).count() + 1

    def get_tokens_ahead(self):
        """Get all tokens ahead in the queue."""
        return Token.objects.filter(
            queue=self.queue,
            token_number__lt=self.token_number,
            status__in=['waiting', 'ready', 'serving']
        ).count()

    class Meta:
        ordering = ['token_number']
        verbose_name_plural = "Tokens"

class Booking(models.Model):
    """Store booking records - separate from tokens for history."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    queue = models.ForeignKey(QueueService, on_delete=models.CASCADE, related_name='bookings')
    token = models.OneToOneField(Token, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Booking: {self.user.username} - {self.queue.service_name}"

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Bookings"

class Notification(models.Model):
    """Store notifications sent to users."""
    NOTIFICATION_TYPES = [
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('both', 'Both'),
    ]
    
    token = models.ForeignKey(Token, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES)
    message = models.TextField()
    is_sent = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Reward(models.Model):
    """Track reward points earned by users."""
    REWARD_REASONS = [
        ('completion', 'Service Completion'),
        ('bonus', 'Bonus Points'),
        ('referral', 'Referral'),
        ('promotion', 'Promotion'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rewards')
    points_earned = models.IntegerField(default=10)
    reason = models.CharField(max_length=20, choices=REWARD_REASONS, default='completion')
    token = models.ForeignKey(Token, on_delete=models.SET_NULL, null=True, blank=True, related_name='rewards')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} earned {self.points_earned} points"

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Rewards"
