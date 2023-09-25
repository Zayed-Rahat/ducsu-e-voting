from .models import Candidate
from django.forms import ModelForm,Textarea
from django import forms
class CandidateForm(ModelForm):   
    class Meta:
        model = Candidate
        fields = ['full_name', 'photo', 'bio', 'position']
        widgets = {
            'bio': Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }
        labels = {
            'full_name': 'Full Name',  # Corrected label here
            'photo': 'Upload Your Image',
            'bio': 'Add Bio',
            'position': 'Add Position',
        }