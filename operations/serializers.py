from rest_framework import serializers
from .models import Account, Category, Operation


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class OperationSerializer(serializers.ModelSerializer):
    account = AccountSerializer()
    category = CategorySerializer()

    class Meta:
        model = Operation
        fields = '__all__'