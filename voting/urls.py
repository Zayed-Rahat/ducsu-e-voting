from django.urls import path
from . import views

urlpatterns = [
    path('ballot/fetch/', views.fetch_ballot, name='fetch_ballot'),
<<<<<<< HEAD
    # path('dashboard/', views.voter_dashboard, name='voterDashboard'),
    path('ballot/fetch/', views.fetch_ballot, name='fetch_ballot'),
    path('dashboard/', views.dashboard, name='voterDashboard'),
=======
    path('myprofile/', views.userProfile, name='userProfile'),
>>>>>>> 1beeaf460289807874f10e8eb0663a3edbfed47b
    path('ballot/vote', views.show_ballot, name='show_ballot'),
    path('ballot/vote/preview', views.preview_vote, name='preview_vote'),
    path('ballot/vote/submit', views.submit_ballot, name='submit_ballot'),
]
