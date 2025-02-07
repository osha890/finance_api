from http.client import responses

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Account


class AccountTests(TestCase):
    prefix = "/api/accounts/"

    def setUp(self):
        self.account = Account.objects.create(name="Test Account", balance=1000)
        self.client = APIClient()

    def test_get_accounts(self):
        response = self.client.get(self.prefix)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_account(self):
        data = {
            "name": "New Account",
            "balance": 1000
        }
        response = self.client.post(self.prefix, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Account.objects.count(), 2)

    def test_update_account(self):
        data = {
            "name": "Updated Account",
            "balance": 2000
        }
        response = self.client.put("{}{}/".format(self.prefix, self.account.id), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, data.get("balance"))

    def test_delete_account(self):
        response = self.client.delete("{}{}/".format(self.prefix, self.account.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Account.objects.count(), 0)
