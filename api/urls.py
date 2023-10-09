from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'position', views.PositionList,basename="position")
router.register(r'voter', views.VoterList,basename="voter")
router.register(r'candidate', views.CandidateList,basename="candidate")
router.register(r'vote', views.VoteList,basename="vote")

# The API URLs are now determined automatically by the router.
urlpatterns = [
    # path('position/', views.PositionListView.as_view()),
    # path('position/<int:pk>/', views.PositionListUpdateDelete.as_view()),
    path('position/', views.PositionList.as_view()),
    path('position/<int:pk>/', views.PositionDeleteUpdate.as_view()),
    path('voter/', views.VoterList.as_view()),
    path('voter/<int:pk>/', views.VoterDeleteUpdate.as_view()),
    path('candidate/', views.CandidateList.as_view()),
    path('candidate/<int:pk>/', views.CandidateDeleteUpdate.as_view()),
    path('vote/', views.VoteList.as_view()),
    path('vote/<int:pk>/', views.VoteDeleteUpdate.as_view()),
]

