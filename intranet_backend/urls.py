from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('intranet.urls')), 
    path('api/', include('resources.urls')),
    path("api/", include('messenger.urls')),
    path('api/', include('meetings.urls')),
    
    ]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
