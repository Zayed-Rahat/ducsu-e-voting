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
        fields = ['verified', 'election']

    # def __init__(self, *args, **kwargs):
    #     super(VoterForm, self).__init__(*args, **kwargs)
    #     if self.instance.pk:
    #         user = self.instance.user
    #         self.fields['election'].queryset = Election.objects.filter(admin=user)

class CandidateForm(FormSettings):    
    class Meta:
        model = Candidate
        fields = ['position', 'fullname', 'bio', 'photo']

    # def __init__(self, *args, **kwargs):
    #     # user = kwargs.pop('user', None)
    #     super(CandidateForm, self).__init__(*args, **kwargs)
    #     if self.instance.pk:
    #         election = Election.objects.get(admin=self.instance.admin)
    #             # election = Election.objects.get(admin=user)
    #         self.fields['position'].queryset = Position.objects.filter(election_id=election.id) 

class VoteForm(FormSettings):
    class Meta:
        model = Vote
        fields = ['election', 'voter', 'position', 'candidate']
