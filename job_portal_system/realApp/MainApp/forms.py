from django import forms
from .models import Job, JobApplication
class JobForm(forms.Form):
    title = forms.CharField(max_length=255)
    description = forms.CharField(widget=forms.Textarea)
    location = forms.CharField(max_length=255)
    salary = forms.DecimalField(max_digits=10, decimal_places=2)


class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['job']
        widgets = {
            'job': forms.Select(),  # Or use forms.RadioSelect if you want to list them
        }
