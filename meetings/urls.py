from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MeetingViewSet, AgendaItemViewSet, DocumentViewSet, generate_boardpack, AnnotationViewSet

router = DefaultRouter()
router.register(r'meetings', MeetingViewSet)
router.register(r'agenda-items', AgendaItemViewSet)
router.register(r'documents', DocumentViewSet)
router.register(r'annotations', AnnotationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('meetings/<int:meeting_id>/boardpack/', generate_boardpack, name='generate_boardpack'),
]