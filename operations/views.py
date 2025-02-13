from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware, get_current_timezone
from django_filters import rest_framework as filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets

from . import messages
from .filters import OperationFilter
from .serializers import AccountSerializer, CategorySerializer, OperationSerializer
from .models import Account, Category, Operation, Type


# Create your views here.

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Category.objects.filter(user=self.request.user)
        type_param = self.request.query_params.get('type')
        if type_param in dict(Type.choices):
            queryset = queryset.filter(type=type_param)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


def set_tz(date):
    date = parse_datetime(date)
    if date and date.tzinfo is None:
        date = make_aware(date, get_current_timezone())
    return date


def get_total_amount(queryset):
    total_amount = 0
    for operation in queryset:
        if operation.type == Type.EXPENSE:
            total_amount -= operation.amount
        elif operation.type == Type.INCOME:
            total_amount += operation.amount
        else:
            pass
    return total_amount


def create_response_with_total_amount(queryset, serializer):
    if queryset:
        total_amount = get_total_amount(queryset)
        return Response({
            'total_amount': total_amount,
            'operations': serializer.data
        })
    return Response([])


class OperationViewSet(viewsets.ModelViewSet):
    queryset = Operation.objects.all()
    serializer_class = OperationSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = OperationFilter
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def recent(self, request):
        queryset = Operation.objects.all()
        type_param = request.query_params.get('type')
        if type_param in dict(Type.choices):
            queryset = queryset.filter(type=type_param)

        count = request.query_params.get('count', 5)
        try:
            count = int(count)
            if count <= 0:
                return Response({"error": messages.NOT_A_VALID_NUMBER}, status=400)
        except ValueError:
            return Response({"error": messages.NOT_A_VALID_NUMBER}, status=400)

        queryset = queryset.order_by('-date')[:count]
        serializer = self.get_serializer(queryset, many=True)

        response = create_response_with_total_amount(queryset, serializer)
        return response

    def get_queryset(self):
        queryset = Operation.objects.filter(user=self.request.user)
        date_after = self.request.query_params.get('date_after')
        date_before = self.request.query_params.get('date_before')

        if date_after:
            date_after = set_tz(date_after)
            queryset = queryset.filter(date__gte=date_after)

        if date_before:
            date_before = set_tz(date_before)
            queryset = queryset.filter(date__lte=date_before)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).order_by('-date')
        serializer = self.get_serializer(queryset, many=True)

        response = create_response_with_total_amount(queryset, serializer)
        return response

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
