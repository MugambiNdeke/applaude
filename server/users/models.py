from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    """
    Custom User model to store essential user data, including the GitHub API token
    required for cloning repos and creating Pull Requests[cite: 98].
    """
    # The GitHub token is securely stored and is essential for the platform's core function.
    github_access_token = models.CharField(max_length=512, blank=True, null=True, 
                                           help_text="GitHub token for PR/Cloning operations.")
    
    # We can add a simple field to track the connected GitHub username
    github_username = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return self.email or self.username

    
class Subscription(models.Model):
    """
    Tracks the user's active plan and the number of autonomous runs remaining.
    """
    PLAN_CHOICES = (
        ('WEEKLY', 'Weekly Sprint'),
        ('MONTHLY', 'Monthly Startup'),
        ('YEARLY', 'Yearly Scale-Up'),
    )
    STATUS_CHOICES = (
        ('ACTIVE', 'Active'),
        ('PENDING', 'Pending Payment'),
        ('CANCELED', 'Canceled'),
        ('EXPIRED', 'Expired'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscription')
    plan = models.CharField(max_length=50, choices=PLAN_CHOICES)
    runs_remaining = models.IntegerField(default=0, help_text="Number of runs left this cycle.")
    
    paystack_reference = models.CharField(max_length=255, blank=True, null=True, 
                                          help_text="Reference for the payment/subscription.")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='PENDING')
    
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.email} - {self.plan} ({self.status})"
