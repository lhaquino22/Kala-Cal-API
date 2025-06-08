from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CasoViewSet

router = DefaultRouter()
router.register(r'casos', CasoViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
] 