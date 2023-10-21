from django import forms
from api.models import *
from account.forms import FormSettings


class PositionForm(FormSettings):
    class Meta:
        model = Position
        fields = ['name', 'max_vote', 'priority']

class ElectionForm(FormSettings):
    class Meta:
        model = Election
        fields = ['title', 'start_date', 'end_date', 'admin']

class VoterForm(FormSettings):
    class Meta:
        model = Voter
        fields = ['election' , 'account_type']

class CandidateForm(FormSettings):
    class Meta:
        model = Candidate
        fields = ['position', 'fullname', 'bio']

class VoteForm(FormSettings):
    class Meta:
        model = Vote
        fields = ['election', 'voter', 'position', 'candidate']
