from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PersonViewSet, HistoryViewSet, RFID1ViewSet, RFID2ViewSet
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register('person', PersonViewSet, basename='person')
router.register('history', HistoryViewSet, basename='history')
router.register('rfid1', RFID1ViewSet, basename='rfid1')
router.register('rfid2', RFID2ViewSet, basename='rfid2')
urlpatterns = router.urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)