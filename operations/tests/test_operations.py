import pytest
from django.urls import reverse

from ..models import Operation, Type
from .fixtures import user, client, account, category_expense, category_income, operation_expense, \
    operation_income, few_operations


@pytest.mark.django_db
def test_operation_expense_create(client, account, category_expense):
    url = reverse("operation-list")
    response = client.post(url, {"type": Type.EXPENSE, "amount": 100, "account": account.id,
                                 "category": category_expense.id})
    assert response.status_code == 201
    assert response.data["amount"] == "100.00"


@pytest.mark.django_db
def test_operation_income_create(client, account, category_income):
    url = reverse("operation-list")
    response = client.post(url, {"type": Type.INCOME, "amount": 300, "account": account.id,
                                 "category": category_income.id})
    assert response.status_code == 201
    assert response.data["amount"] == "300.00"


@pytest.mark.django_db
def test_operation_empty_list(client):
    url = reverse("operation-list")
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 0


@pytest.mark.django_db
def test_operation_ist(client, operation_expense, operation_income):
    url = reverse("operation-list")
    response = client.get(url)
    assert response.status_code == 200
    assert response.data.get("total_amount") == -100
    assert len(response.data.get("operations")) == 2


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


@pytest.mark.django_db
def test_operations_recent_default(client, few_operations):
    url = reverse("operation-recent")
    response = client.get(url)
    assert len(response.data.get("operations")) == 5
    assert response.data.get("total_amount") == 550


@pytest.mark.django_db
def test_operations_recent(client, few_operations):
    url = reverse("operation-recent") + "?count=3"
    response = client.get(url)
    assert len(response.data.get("operations")) == 3
    assert response.data.get("total_amount") == 100
