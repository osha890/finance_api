from rest_framework import serializers
from .models import Account, Category, Operation
from . import messages


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ['is_default']


class OperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operation
        fields = '__all__'

    def validate(self, data):
        category = data['category']
        if category.type != data['type']:
            raise serializers.ValidationError(messages.WRONG_CATEGORY.format(category=category))
        return data
