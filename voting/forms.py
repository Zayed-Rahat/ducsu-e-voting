from django import forms
from api.models import *
from account.forms import FormSettings
from django.contrib.admin.widgets import AdminSplitDateTime


class PositionForm(FormSettings):
    class Meta:
        model = Position
        fields = ['name', 'max_vote', 'priority']



   

class DateTimeInput(forms.DateTimeInput):
    input_type = "datetime-local"
    def __init__(self, **kwargs):
        kwargs["format"] = "%Y-%m-%dT%H:%M"
        super().__init__(**kwargs)

class ElectionForm(FormSettings):
    class Meta:
        model = Election
        fields = ['title', 'start_date', 'end_date']
        widgets = {            
            'start_date': DateTimeInput(format=["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"],),
            'end_date': DateTimeInput(format=["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"],),   

        }
      


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

class VoteForm(FormSettings):
    class Meta:
        model = Vote
        fields = ['election', 'voter', 'position', 'candidate']
