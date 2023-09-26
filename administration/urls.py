from django.urls import path
from . import views
urlpatterns = [
    path('',views.dashboard,name='dashboard'),
    path('position/',views.position, name='position'),
    path('add_position/',views.add_position, name='add_position'),
    path('edit_position/<int:id>/',views.edit_position, name='edit_position'),
    path('delete_position/<int:id>/',views.delete_position, name='delete_position'),
]
