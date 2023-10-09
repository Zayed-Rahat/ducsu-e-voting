from .models import Position
from .serializers import PositionSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status



from .models import Position,Voter,Candidate,Vote
from .serializers import PositionSerializer,VoterSerializer,CandidateSerializer,VoteSerializer
from rest_framework import generics


class PositionList(generics.ListCreateAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
class VoterList(generics.ListCreateAPIView):
    queryset = Voter.objects.all()
    serializer_class = VoterSerializer
class CandidateList(generics.ListCreateAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
class VoteList(generics.ListCreateAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer


class PositionDeleteUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
class VoterDeleteUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Voter.objects.all()
    serializer_class = VoterSerializer
class CandidateDeleteUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
class VoteDeleteUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer