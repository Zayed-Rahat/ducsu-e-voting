from django.urls import path
from . import views
urlpatterns = [
    # path('',views.dashboard,name='dashboard'),
    path('position/',views.position, name='position'),
    path('add_position/',views.add_position, name='add_position'),
    path('edit_position/<int:id>/',views.edit_position, name='edit_position'),
    path('delete_position/<int:id>/',views.delete_position, name='delete_position'),

    path('voters/',views.voters, name='voters'),
    path('edit_voter/<int:id>/',views.edit_voter, name='edit_voter'),
    path('delete_voter/<int:id>/',views.delete_voter, name='delete_voter'),
    
    
    path('candidate/',views.show_candidate, name='candidate'),
    path('add_candidate/',views.create_candidate, name='add_candidate'),
    path('edit_candidate/<int:id>/',views.edit_voter, name='edit_candidate'),
    path('delete_candidate/<int:id>/',views.delete_voter, name='delete_candidate'),
    
    
]
