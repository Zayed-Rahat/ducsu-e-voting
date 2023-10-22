from django.urls import path
from . import views


urlpatterns = [
    # path('login/', views.account_login, name="account_login"),
    # path('register/', views.account_register, name="account_register"),
    path('logout/', views.account_logout, name="account_logout"),
    path('change_pass/', views.change_pass, name="change_pass"),
    
    # team profile user
    path('profile/',views.profile, name='profile'),
    path('about/',views.aboutus, name='about'),
    
    
    # my code authentication
    path('login/',views.account_login, name='login'),
    path('register/',views.account_register, name='register'),
    # path('logout/',views.user_logout, name='logout'),
]
