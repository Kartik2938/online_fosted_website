from django.db import models
from django.conf import settings


class Job(models.Model):
    job_id = models.AutoField(primary_key=True)
    job_title = models.CharField(max_length=100)
    job_description = models.TextField()
    pub_date = models.DateField()

    CATEGORY_CHOICES = [
        ('it', 'IT & Software'),
        ('finance', 'Finance'),
        ('marketing', 'Marketing'),
        ('education', 'Education'),
        ('healthcare', 'Healthcare'),
        ('engineering', 'Engineering'),
        ('construction', 'Construction'),
        ('legal', 'Legal'),
        ('retail', 'Retail'),
        ('hospitality', 'Hospitality'),
        ('government', 'Government'),
        ('arts', 'Arts & Media'),
        ('others', 'Others'),
    ]

    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.job_title


# 💾 Saved Jobs (like a cart)
# models.py
class SavedJobs(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='saved_jobs')
    jobs = models.ManyToManyField(Job, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # ✅ Add this

    def __str__(self):
        return f"{self.user.username}'s Saved Jobs"


# 📄 Job Application (like an order)
class JobApplication(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Reviewed', 'Reviewed'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.user.username} - {self.job.job_title} - {self.status}"
