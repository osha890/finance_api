from django.db.models import ProtectedError, Subquery
from django_filters import rest_framework as filters

from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets, status

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
        return get_queryset_for_user(self.request.user, Account).order_by('id')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
        except ProtectedError:
            return Response(
                {"error": messages.ACCOUNT_PROTECTED_ERROR},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = get_queryset_for_user(self.request.user, Category)

        type_param = self.request.query_params.get('type')
        if type_param in dict(Type.choices):
            queryset = queryset.filter(type=type_param)
        return queryset.order_by('id')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def deny_access_if_default_and_not_stuff(self, request):
        category = self.get_object()
        if category.is_default and not request.user.is_staff:
            raise PermissionDenied(messages.DEFAULT_CATEGORY_CHANGE)

    def destroy(self, request, *args, **kwargs):
        self.deny_access_if_default_and_not_stuff(request)
        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self.deny_access_if_default_and_not_stuff(request)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        self.deny_access_if_default_and_not_stuff(request)
        return super().partial_update(request, *args, **kwargs)


class OperationViewSet(viewsets.ModelViewSet):
    queryset = Operation.objects.all()
    serializer_class = OperationSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = OperationFilter
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def recent(self, request):
        queryset = get_queryset_for_user(self.request.user, Operation)

        type_param = request.query_params.get('type')
        if type_param in dict(Type.choices):
            queryset = queryset.filter(type=type_param)

        count = request.query_params.get('count', 5)
        response = Response({"error": messages.NOT_A_VALID_NUMBER}, status=400)
        try:
            count = int(count)
            if count <= 0:
                return response
        except ValueError:
            return response

        latest_records = queryset.order_by('-date')[:count]
        queryset = queryset.filter(id__in=Subquery(latest_records.values('id'))).order_by('date')

        serializer = self.get_serializer(queryset, many=True)

        response = create_response_with_total_amount(queryset, serializer)
        return response

    def get_queryset(self):
        queryset = get_queryset_for_user(self.request.user, Operation)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).order_by('date')
        serializer = self.get_serializer(queryset, many=True)

        response = create_response_with_total_amount(queryset, serializer)
        return response

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
