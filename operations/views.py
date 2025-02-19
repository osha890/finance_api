from django_filters import rest_framework as filters

from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets

from . import messages
from .filters import OperationFilter
from .serializers import AccountSerializer, CategorySerializer, OperationSerializer
from .models import Account, Category, Operation, Type
from .utils import get_queryset_for_user, set_tz, create_response_with_total_amount


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return get_queryset_for_user(self.request.user, Account)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = get_queryset_for_user(self.request.user, Category)

        type_param = self.request.query_params.get('type')
        if type_param in dict(Type.choices):
            queryset = queryset.filter(type=type_param)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        category = self.get_object()
        if category.is_default and not request.user.is_staff:
            raise PermissionDenied(messages.DEFAULT_CATEGORY_DELETE)

        return super().destroy(request, *args, **kwargs)


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
        queryset = get_queryset_for_user(self.request.user, Operation)

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
