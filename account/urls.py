from django.urls import path 
from . import views

urlpatterns = [
    path('login/',views.user_login, name='login'),
    path('register/',views.user_registration, name='register'),
    path('logout/',views.user_logout, name='logout'),
    
    # update password with old password
    # path('pass_change/',views.pass_change, name='pass_change'),
    # update password without old password
    # path('change_pass/',views.change_pass, name='change_pass'),
    
    
    # activate account in email
    # path('activate/<uidb64>/<token>/',views.activate, name='activate'),
    
]
