from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet
from .views import UserInvitationViewSet,CurrentUserViewSet,ResetPasswordViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'me', CurrentUserViewSet, basename='current_user')
router.register(r'invite', UserInvitationViewSet, basename='user-invitation')
router.register(r'password-reset', ResetPasswordViewSet, basename='password-reset')


urlpatterns = [
    path('', include(router.urls)),
    path('reset-password/<uidb64>/<token>/', ResetPasswordViewSet.as_view({'post': 'reset_password'}), name='reset-password'),
    
    
]

urlpatterns += router.urls