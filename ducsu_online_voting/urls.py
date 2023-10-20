from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from .views import home
from . import settings

urlpatterns = [
    path('',home, name='home'),
    # path('', include('account.urls')),
    path('account/', include('account.urls')),
    path('admin/', admin.site.urls),
    path('administrator/', include('administration.urls')),
    path('voting/', include('voting.urls')),
    path('api/', include('api.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
