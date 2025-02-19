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
def category_expense(user):
    return Category.objects.create(name="Test Category expense", type=Type.EXPENSE, user=user)


@pytest.fixture
def category_income(user):
    return Category.objects.create(name="Test Category income", type=Type.INCOME, user=user)


@pytest.fixture
def operation(user, account, category_expense):
    return Operation.objects.create(type=Type.EXPENSE, amount=200, account=account, category=category_expense,
                                    user=user)


# ======== Accounts tests ========

@pytest.mark.django_db
def test_account_create(client):
    url = reverse("account-list")
    response = client.post(url, {"name": "New Account", "balance": 500})
    assert response.status_code == 201
    assert response.data["name"] == "New Account"


@pytest.mark.django_db
def test_account_list(client, account):
    url = reverse("account-list")
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["name"] == account.name


@pytest.mark.django_db
def test_account_delete(client, account):
    url = reverse("account-detail", args=[account.id])
    response = client.delete(url)
    assert response.status_code == 204
    assert len(Account.objects.all()) == 0


# ======== Categories tests ========

@pytest.mark.django_db
def test_category_create(client):
    url = reverse("category-list")
    response = client.post(url, {"name": "Food", "type": Type.EXPENSE})
    assert response.status_code == 201
    assert response.data["name"] == "Food"


@pytest.mark.django_db
def test_category_list(client, category_expense):
    url = reverse("category-list")
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 3
    assert response.data[2]["name"] == category_expense.name


@pytest.mark.django_db
def test_category_delete(client, category_expense):
    url = reverse("category-detail", args=[category_expense.id])
    response = client.delete(url)
    assert response.status_code == 204
    assert len(Category.objects.filter(id=category_expense.id)) == 0


@pytest.mark.django_db
def test_category_delete_default(client, user):
    category_default = Category.objects.filter(is_default=True, user=user).first()
    url = reverse("category-detail", args=[category_default.id])
    response = client.delete(url)
    assert response.status_code == 403
    assert len(Category.objects.filter(is_default=True, user=user)) == 2


@pytest.mark.django_db
def test_category_with_operations_delete(client, category_expense, operation):
    url = reverse("category-detail", args=[category_expense.id])
    response = client.delete(url)
    assert response.status_code == 204
    operation.refresh_from_db()
    assert operation.category != category_expense


# ======== Operations tests ========

@pytest.mark.django_db
def test_operation_create(client, account, category_expense):
    url = reverse("operation-list")
    response = client.post(url, {"type": Type.EXPENSE, "amount": 100, "account": account.id,
                                 "category": category_expense.id})
    assert response.status_code == 201
    assert response.data["amount"] == "100.00"


@pytest.mark.django_db
def test_operation_list(client):
    url = reverse("operation-list")
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 0


@pytest.mark.django_db
def test_operation_expense_affects_balance(client, account, category_expense):
    initial_balance = account.balance
    url = reverse("operation-list")
    client.post(url, {"type": Type.EXPENSE, "amount": 100, "account": account.id, "category": category_expense.id})
    account.refresh_from_db()
    assert account.balance == initial_balance - 100


@pytest.mark.django_db
def test_operation_income_affects_balance(client, account, category_income):
    initial_balance = account.balance
    url = reverse("operation-list")
    client.post(url, {"type": Type.INCOME, "amount": 200, "account": account.id, "category": category_income.id})
    account.refresh_from_db()
    assert account.balance == initial_balance + 200


@pytest.mark.django_db
def test_operation_create_wrong_type(client, account, category_income):
    url = reverse("operation-list")
    response = client.post(url,
                           {"type": Type.EXPENSE, "amount": 200, "account": account.id, "category": category_income.id})
    account.refresh_from_db()
    assert response.status_code == 400
    assert len(Operation.objects.all()) == 0
