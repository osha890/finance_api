import pytest
from django.urls import reverse

from ..models import Category, Type
from .fixtures import user, client, account, category_expense, category_income, operation_expense, \
    operation_income, few_operations


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
def test_category_with_operations_delete(client, category_expense, operation_expense):
    url = reverse("category-detail", args=[category_expense.id])
    response = client.delete(url)
    assert response.status_code == 204
    operation_expense.refresh_from_db()
    assert operation_expense.category != category_expense
