import pytest
from django.urls import reverse

from ..models import Account
from .fixtures import user, client, account, category_expense, category_income, operation_expense, \
    operation_income, few_operations


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
