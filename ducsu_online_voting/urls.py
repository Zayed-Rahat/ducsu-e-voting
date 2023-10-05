# 
from django.contrib import admin
from django.urls import path,  include 
from django.conf.urls.static import static
from django.conf import settings
from . import views
urlpatterns = [
    path('',views.home, name='home'),
    path('admin/', admin.site.urls),
    path('administration/',include('administration.urls') ),
    path('account/', include('account.urls')),
<<<<<<< HEAD
    path('api/', include('api.urls')),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
=======
    
]+ static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT)
>>>>>>> 1528ee7ed751ae0f44d211e0e8c849146c7ebf86
