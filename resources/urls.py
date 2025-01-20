from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ResourceViewSet

router = DefaultRouter()
router.register(r'folders', ResourceViewSet, basename='Folders')

urlpatterns = [
    path('', include(router.urls)),
    path('nested_folders/', ResourceViewSet.as_view({'get': 'nested_folders'}), name='nested_folders'),
    path('children/<int:pk>/', ResourceViewSet.as_view({'get': 'children'}), name='children'),
    path('rename/<int:pk>/', ResourceViewSet.as_view({'post': 'rename'}), name='rename'),
    
]