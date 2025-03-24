from rest_framework import serializers

from .models import Account, Category, Operation
from . import messages


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'name', 'balance', 'user']
        read_only_fields = ['user']

    def validate(self, data):
        """Валидация на существование счета с таким же именем у пользователя"""
        validate_existence(self.context['request'].user, data, Account)
        return data


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'type', 'user']
        read_only_fields = ['is_default', 'user']

    def validate(self, data):
        """Валидация на существование категории с таким же именем у пользователя"""
        validate_existence(self.context['request'].user, data, Category)
        return data


class OperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operation
        fields = ['id', 'type', 'amount', 'account', 'category', 'description', 'date', 'user']
        read_only_fields = ['user']

    def validate(self, data):
        """Проверка корректности введенных данных перед сохранением операции"""
        user = self.context['request'].user
        account = data.get('account')
        category = data.get('category')
        operation_type = data.get('type')

        # Проверяем, принадлежит ли счет пользователю
        if account is not None:
            if account.user != user:
                raise serializers.ValidationError(messages.WRONG_USER_ACCOUNT)

        # Проверяем, принадлежит ли категория пользователю
        if category is not None:
            if category.user != user:
                raise serializers.ValidationError(messages.WRONG_USER_CATEGORY)

        # Проверяем, соответствует ли тип операции типу категории
        if category is not None and operation_type is not None:
            if category.type != operation_type:
                raise serializers.ValidationError(messages.WRONG_CATEGORY.format(category=category))

        return data


def validate_existence(user, data, model):
    """Функция валидации на уникальность имени объекта у пользователя"""
    name = data.get('name')
    if name is not None:
        # Проверяем, существует ли объект с таким именем у данного пользователя
        if model.objects.filter(user=user, name=name).exists():

            # Генерируем текст для ошибки
            if model == Account:
                error_message = messages.ACCOUNT_ALREADY_EXISTS
            elif model == Category:
                error_message = messages.CATEGORY_ALREADY_EXISTS
            else:
                error_message = "error"

            raise serializers.ValidationError({"name": error_message})
