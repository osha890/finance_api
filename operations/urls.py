from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AccountViewSet, CategoryViewSet, OperationViewSet

router = DefaultRouter()
router.register(r'accounts', AccountViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'operations', OperationViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
