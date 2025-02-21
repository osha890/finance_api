from rest_framework import serializers

from .models import Account, Category, Operation
from . import messages


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'name', 'balance', 'user']
        read_only_fields = ['user']

    def validate(self, data):
        validate_existence(self.context['request'].user, data, Account)
        return data


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'type', 'user']
        read_only_fields = ['is_default', 'user']

    def validate(self, data):
        validate_existence(self.context['request'].user, data, Category)
        return data


class OperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operation
        fields = ['id', 'type', 'amount', 'account', 'category', 'description', 'date', 'user']
        read_only_fields = ['user']

    def validate(self, data):
        user = self.context['request'].user
        account = data.get('account')
        category = data.get('category')
        operation_type = data.get('type')

        if account is not None:
            if account.user != user:
                raise serializers.ValidationError(messages.WRONG_USER_ACCOUNT)
        if category is not None:
            if category.user != user:
                raise serializers.ValidationError(messages.WRONG_USER_CATEGORY)
        if category is not None and operation_type is not None:
            if category.type != operation_type:
                raise serializers.ValidationError(messages.WRONG_CATEGORY.format(category=category))

        return data


def validate_existence(user, data, model):
    name = data.get('name')
    if name is not None:
        if model == Account:
            error_message = messages.ACCOUNT_ALREADY_EXISTS
        elif model == Category:
            error_message = messages.CATEGORY_ALREADY_EXISTS
        else:
            error_message = "error"
        if model.objects.filter(user=user, name=name).exists():
            raise serializers.ValidationError({"name": error_message})
