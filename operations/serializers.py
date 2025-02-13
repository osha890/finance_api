from rest_framework import serializers

from .models import Account, Category, Operation
from . import messages


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'name', 'balance']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'type']
        read_only_fields = ['is_default']


class OperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operation
        fields = ['id', 'type', 'amount', 'account', 'category', 'description', 'date']

    def validate(self, data):
        category = data['category']
        if category.type != data['type']:
            raise serializers.ValidationError(messages.WRONG_CATEGORY.format(category=category))
        return data
