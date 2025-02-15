from django.urls import path
from .views import RegisterView, UserListView

urlpatterns = [
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/users/', UserListView.as_view(), name='users'),
]
