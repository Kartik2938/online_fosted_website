from django.contrib import admin
from .models import Job, SavedJobs, JobApplication

# 🧾 Admin for Job
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('job_id', 'job_title', 'category', 'pub_date')
    list_filter = ('category', 'pub_date')
    search_fields = ('job_title', 'category')
    radio_fields = {'category': admin.VERTICAL}

# 💾 Admin for Saved Jobs
@admin.register(SavedJobs)
class SavedJobsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'display_jobs')
    filter_horizontal = ('jobs',)

    def display_jobs(self, obj):
        return ", ".join([job.job_title for job in obj.jobs.all()])
    display_jobs.short_description = "Saved Jobs"

# 📄 Admin for Job Application
@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'job', 'applied_at', 'status')
    list_filter = ('status', 'applied_at')
    search_fields = ('user__username', 'job__job_title')
