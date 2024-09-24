# In your messaging/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MessageViewSet

router = DefaultRouter()
router.register(r'messages', MessageViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('messages/users/', MessageViewSet.as_view({'get': 'users'}), name='user-list'),
]
