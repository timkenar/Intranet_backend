from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet
from .views import UserInvitationView,CurrentUserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'me', CurrentUserViewSet, basename='current_user')


urlpatterns = [
    path('', include(router.urls)),
    path('invite/', UserInvitationView.as_view(), name='user_invitation'),
]