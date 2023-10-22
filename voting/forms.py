from django import forms
from api.models import *
from account.forms import FormSettings


class PositionForm(FormSettings):
    class Meta:
        model = Position
        fields = ['name', 'max_vote', 'priority']

class ElectionForm(FormSettings):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    class Meta:
        model = Election
        fields = ['title', 'start_date', 'end_date']

class VoterForm(FormSettings):
    class Meta:
        model = Voter
        fields = ['election' , 'account_type']


class CandidateForm(FormSettings):    
    class Meta:
        model = Candidate
        fields = ['position', 'fullname', 'bio', 'photo']

    # def __init__(self, *args, **kwargs):
    #     super(CandidateForm, self).__init__(*args, **kwargs)
    #     if self.instance.pk:
    #         self.fields['position'].queryset = Position.objects.get(election_id=self.election_id)
    #     else:
    #         self.fields['position'].queryset = Position.objects.none()    
# class CandidateForm(FormSettings):
#     def __init__(self, *args, **kwargs):
#         # Extract the 'election' parameter from kwargs
#         election = kwargs.pop('election', None)
#         super(CandidateForm, self).__init__(*args, **kwargs)

#         # Set the election as an instance variable
#         self.election = election

#     class Meta:
#         model = Candidate
#         fields = ['position', 'fullname', 'bio', 'photo']  # Add the fields you want to include in the form

#     def clean(self):
#         cleaned_data = super().clean()
#         # Perform your custom validation here
#         # Access the election instance using self.election

#         # Example validation logic:
#         # if some_condition:
#         #     raise forms.ValidationError("Validation error message")

#         return cleaned_data
class VoteForm(FormSettings):
    class Meta:
        model = Vote
        fields = ['election', 'voter', 'position', 'candidate']
