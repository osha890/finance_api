import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from operations.models import Account, Category, Operation, Type
from django.urls import reverse

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
def category(user):
    return Category.objects.create(name="Test Category", type=Type.EXPENSE, user=user)

@pytest.fixture
def operation(user, account, category):
    return Operation.objects.create(type=Type.EXPENSE, amount=200, account=account, category=category, user=user)

@pytest.mark.django_db
def test_create_account(client):
    url = reverse("account-list")
    response = client.post(url, {"name": "New Account", "balance": 500})
    assert response.status_code == 201
    assert response.data["name"] == "New Account"

@pytest.mark.django_db
def test_list_accounts(client, account):
    url = reverse("account-list")
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["name"] == account.name

@pytest.mark.django_db
def test_create_category(client):
    url = reverse("category-list")
    response = client.post(url, {"name": "Food", "type": Type.EXPENSE})
    assert response.status_code == 201
    assert response.data["name"] == "Food"

@pytest.mark.django_db
def test_create_operation(client, account, category):
    url = reverse("operation-list")
    response = client.post(url, {"type": Type.EXPENSE, "amount": 100, "account": account.id, "category": category.id})
    assert response.status_code == 201
    assert response.data["amount"] == "100.00"

@pytest.mark.django_db
def test_operation_affects_balance(client, account, category):
    initial_balance = account.balance
    url = reverse("operation-list")
    client.post(url, {"type": Type.EXPENSE, "amount": 100, "account": account.id, "category": category.id})
    account.refresh_from_db()
    assert account.balance == initial_balance - 100

@pytest.mark.django_db
def test_delete_category_with_operations(client, category, operation):
    url = reverse("category-detail", args=[category.id])
    response = client.delete(url)
    assert response.status_code == 204
    operation.refresh_from_db()
    assert operation.category != category
