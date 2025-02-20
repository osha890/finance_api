import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework.authtoken.models import Token

User = get_user_model()


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def create_user(db):
    def make_user(**kwargs):
        return User.objects.create_user(**kwargs)
    return make_user


# ======== User test ========

@pytest.mark.django_db
def test_user_register(client):
    url = reverse("register")
    data = {"username": "testuser", "password": "testpass"}

    response = client.post(url, data)

    assert response.status_code == 201
    assert "token" in response.data
    assert User.objects.filter(username="testuser").exists()


@pytest.mark.django_db
def test_user_list_unauthorized(client):
    url = reverse("user-list")

    response = client.get(url)

    assert response.status_code == 401


@pytest.mark.django_db
def test_user_list_not_admin(client, create_user):
    user = create_user(username="user", password="userpass", is_staff=False)
    token = Token.objects.create(user=user)
    client.credentials(HTTP_AUTHORIZATION = f"Token {token.key}")

    url = reverse("user-list")
    response = client.get(url)

    assert response.status_code == 403


@pytest.mark.django_db
def test_user_list_admin(client, create_user):
    admin_user = create_user(username="admin", password="adminpass", is_staff=True)
    token = Token.objects.create(user=admin_user)
    client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    url = reverse("user-list")
    response = client.get(url)

    assert response.status_code == 200
    assert isinstance(response.data, list)
