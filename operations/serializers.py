from rest_framework import serializers
from .models import Account, Category, Operation


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['name', 'balance']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'type']


class OperationSerializer(serializers.ModelSerializer):
    account = AccountSerializer()
    category = CategorySerializer()

    class Meta:
        model = Operation
        fields = ['type', 'amount', 'account', 'category', 'description', 'date']
        # fields = '__all__'