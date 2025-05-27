from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth import get_user_model
from datetime import date, datetime

User = get_user_model()

class Job(models.Model):
    # Using Celery beat to regularlyhandle the status of the job
    # by checking if the posting date is in the future or the expiration date is in the past
    STATUS_CHOICES = [
        ("scheduled", "Scheduled"),
        ("active", "Active"),
        ("expired", "Expired"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    salary_range = models.CharField(max_length=100, blank=True)
    company = models.CharField(max_length=255)
    required_skills = ArrayField(models.CharField(max_length=100), blank=True, default=list)
    posting_date = models.DateField()
    expiration_date = models.DateField()

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="scheduled")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-posting_date']

    def save(self, *args, **kwargs):
        today = date.today()

        if isinstance(self.posting_date, datetime):
            self.posting_date = self.posting_date.date()
        if isinstance(self.expiration_date, datetime):
            self.expiration_date = self.expiration_date.date()

        if self.posting_date > today:
            self.status = "scheduled"
        elif self.expiration_date < today:
            self.status = "expired"
        else:
            self.status = "active"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} at {self.company}"
