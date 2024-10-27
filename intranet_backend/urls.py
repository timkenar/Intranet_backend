from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('intranet.urls')), 
    path('api/resource/', include('resources.urls')),
    path("api/message/", include('messenger.urls')),
    path('api/meetings/', include('meetings.urls')),
    path('api/license/', include('license.urls')),
    path('api/directory/', include('directory.urls'))
    
    ]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
