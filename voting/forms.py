from django import forms
from api.models import *
from account.forms import FormSettings
import requests

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

    def __init__(self, *args, **kwargs):
        # user = kwargs.pop('user', None)
        super(CandidateForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            election = Election.objects.get(admin=self.instance.admin)
                # election = Election.objects.get(admin=user)
            self.fields['position'].queryset = Position.objects.filter(election_id=election.id) 

class VoteForm(FormSettings):
    class Meta:
        model = Vote
        fields = ['election', 'voter', 'position', 'candidate']
