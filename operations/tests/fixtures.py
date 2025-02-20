import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from ..models import Account, Category, Operation, Type

User = get_user_model()


@pytest.fixture
def user(db):
    return User.objects.create_user(username="testuser", password="testpass")


@pytest.fixture
def client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def account(user):
    return Account.objects.create(name="Test Account", balance=1000, user=user)


@pytest.fixture
def category_expense(user):
    return Category.objects.create(name="Test Category expense", type=Type.EXPENSE, user=user)


@pytest.fixture
def category_income(user):
    return Category.objects.create(name="Test Category income", type=Type.INCOME, user=user)


@pytest.fixture
def operation_expense(user, account, category_expense):
    return Operation.objects.create(type=Type.EXPENSE, amount=200, account=account, category=category_expense,
                                    user=user)


@pytest.fixture
def operation_income(user, account, category_income):
    return Operation.objects.create(type=Type.INCOME, amount=100, account=account, category=category_income,
                                    user=user)


@pytest.fixture
def few_operations(user, account, category_expense, category_income):
    data_set = [
        {"type": Type.EXPENSE, "amount": 150, "account": account, "category": category_expense, "user": user},
        # Total amount = 200
        {"type": Type.EXPENSE, "amount": 200, "account": account, "category": category_expense, "user": user},
        # Total amount = 350
        {"type": Type.INCOME, "amount": 300, "account": account, "category": category_income, "user": user},
        # Total amount = 550
        {"type": Type.INCOME, "amount": 150, "account": account, "category": category_income, "user": user},
        # Total amount = 250
        {"type": Type.INCOME, "amount": 100, "account": account, "category": category_income, "user": user},
        # Total amount = 100
        {"type": Type.EXPENSE, "amount": 200, "account": account, "category": category_expense, "user": user},
        # Total amount = 0
        {"type": Type.INCOME, "amount": 200, "account": account, "category": category_income, "user": user},
        # Total amount = 200
    ]
    for data in data_set:
        Operation.objects.create(**data)
    return Operation.objects.all()