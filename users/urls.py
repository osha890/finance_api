from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import RegisterView, UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/', include(router.urls)),
]
