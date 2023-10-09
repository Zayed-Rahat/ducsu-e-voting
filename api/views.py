from .models import Position
from .serializers import PositionSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status



from .models import Position,Voter,Candidate,Vote
from .serializers import PositionSerializer,VoterSerializer,CandidateSerializer,VoteSerializer
from rest_framework import generics
from . import paginations


class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    pagination_class = paginations.PositionPagination
class VoterViewSet(viewsets.ModelViewSet):
    queryset = Voter.objects.all()
    serializer_class = VoterSerializer
    pagination_class = paginations.VoterPagination
class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    pagination_class = paginations.VotePagination
class CandidateViewSet(viewsets.ModelViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    pagination_class = paginations.CandidatePagination

class PositionList(generics.ListCreateAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    @staticmethod
    def get_extra_actions():
        return []
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