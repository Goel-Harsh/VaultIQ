from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import FileViewSet, storage_savings

router = DefaultRouter()
router.register(r'files', FileViewSet, basename='file')

urlpatterns = router.urls + [
    path('storage-savings/', storage_savings, name='storage-savings'),
]
