from datetime import datetime

from django.shortcuts import render

from .serializers import AccountSerializer, CategorySerializer, OperationSerializer
from rest_framework import viewsets
from .models import Account, Category, Operation, Type


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


class OperationViewSet(viewsets.ModelViewSet):
    queryset = Operation.objects.all()
    serializer_class = OperationSerializer
