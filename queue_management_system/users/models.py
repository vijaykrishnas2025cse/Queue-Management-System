from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    """Extended user profile with additional information and rewards."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_admin_user = models.BooleanField(default=False)
    reward_points = models.IntegerField(default=0, help_text="Loyalty reward points")
    completed_bookings = models.IntegerField(default=0, help_text="Number of completed bookings")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    def get_priority_score(self):
        """Calculate priority score based on rewards and completed bookings."""
        return self.reward_points + (self.completed_bookings * 5)
    
    def add_reward_points(self, points):
        """Add reward points to user profile."""
        self.reward_points += points
        self.completed_bookings += 1
        self.save()

    class Meta:
        verbose_name_plural = "User Profiles"
        ordering = ['-reward_points']

# Signal to create profile when user is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=instance)
