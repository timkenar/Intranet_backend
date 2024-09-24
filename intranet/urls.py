from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, UserProfileView,  RegisterView, UserProfileView, LoginView, LogoutView, UserListView 
# FileViewSet, FolderViewSet, NotificationViewSet

# router = DefaultRouter()
# router.register(r'files', FileViewSet, basename='file')
# router.register(r'folders', FolderViewSet, basename='folder')
# router.register(r'notifications', NotificationViewSet, basename='notification')

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/profile/', UserProfileView.as_view(), name='profile'),
    path('users/', UserListView.as_view(), name='user-list')
    # path('auth/', include('rest_framework.urls')),  # Login/Logout views

   
]

    # path('api/', include(router.urls)),
