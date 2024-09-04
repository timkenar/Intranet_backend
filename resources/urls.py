from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FileViewSet, FolderViewSet, NotificationViewSet

router = DefaultRouter()
router.register(r'files', FileViewSet, basename='file')
router.register(r'folders', FolderViewSet, basename='folder')
router.register(r'notifications', NotificationViewSet, basename='notification')

urlpatterns = [
    path('', include(router.urls)),
]
