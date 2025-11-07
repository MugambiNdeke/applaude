import uuid
from django.db import models
from django.conf import settings

class Project(models.Model):
    """
    Represents a connected GitHub repository[cite: 7].
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='projects')
    name = models.CharField(max_length=255)
    github_url = models.URLField(max_length=512)
    
    # Simple placeholder for the cloning path on the worker machine
    local_path = models.CharField(max_length=512, blank=True, null=True) 

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Project: {self.name} by {self.user.email}"


class TestRun(models.Model):
    """
    Represents a single autonomous execution by the 3-Agent system.
    """
    STATUS_CHOICES = (
        ('QUEUED', 'Queued'), # 
        ('CLONING', 'Cloning'), # [cite: 121]
        ('TESTING', 'Testing'), # [cite: 126]
        ('DEBUGGING', 'Debugging'), # [cite: 132]
        ('REPORTING', 'Reporting'), # [cite: 139]
        ('COMPLETE', 'Complete'), # [cite: 146]
        ('FAILED', 'Failed'),
    )
    TYPE_CHOICES = (
        ('FULL_STACK', 'Test Full Stack'), # Option A [cite: 110]
        ('FRONTEND_ONLY', 'Test Frontend UI Only'), # Option B [cite: 111]
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='runs')
    
    # Celery task ID for tracking the async job [cite: 117]
    celery_task_id = models.CharField(max_length=255, blank=True, null=True) 
    
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='QUEUED')
    run_type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='FULL_STACK')
    
    # Delivery artifacts [cite: 146]
    pr_url = models.URLField(max_length=512, blank=True, null=True)
    report_url = models.URLField(max_length=512, blank=True, null=True) 
    
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-started_at']

    def __str__(self):
        return f"Run {self.id} on {self.project.name} - {self.status}"
