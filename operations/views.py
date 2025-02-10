from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware, get_current_timezone

from .filters import OperationFilter
from .serializers import AccountSerializer, CategorySerializer, OperationSerializer
from rest_framework import viewsets
from .models import Account, Category, Operation, Type
from django_filters import rest_framework as filters


# Create your views here.

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):
        queryset = Category.objects.all()
        type_param = self.request.query_params.get('type')
        if type_param in dict(Type.choices):
            queryset = queryset.filter(type=type_param)
        return queryset


def set_tz(date):
    date = parse_datetime(date)
    if date and date.tzinfo is None:
        date = make_aware(date, get_current_timezone())
    return date


class OperationViewSet(viewsets.ModelViewSet):
    queryset = Operation.objects.all()
    serializer_class = OperationSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = OperationFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        date_after = self.request.query_params.get('date_after')
        date_before = self.request.query_params.get('date_before')

        if date_after:
            date_after = set_tz(date_after)
            queryset = queryset.filter(date__gte=date_after)
        if date_before:
            date_before = set_tz(date_before)
            queryset = queryset.filter(date__lte=date_before)

        return queryset
