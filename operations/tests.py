import datetime

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from .models import Account, Category, Operation, Type


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


class CategoriesTest(TestCase):
    prefix = "/api/categories/"

    def setUp(self):
        self.category = Category.objects.create(name="Test Category", type=Type.EXPENSE, is_default=False)
        self.client = APIClient()

    def test_get_categories(self):
        response = self.client.get(self.prefix)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_category(self):
        data = {
            "name": "New Category",
            "type": Type.INCOME,
            "is_default": False
        }
        response = self.client.post(self.prefix, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)

    def test_update_category(self):
        data = {
            "name": "Updated Category",
            "type": Type.INCOME,
            "is_default": True
        }
        response = self.client.put("{}{}/".format(self.prefix, self.category.id), data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category.refresh_from_db()
        self.assertEqual(self.category.type, data.get("type"))

    def test_delete_category(self):
        response = self.client.delete("{}{}/".format(self.prefix, self.category.id))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), 0)


class OperationsTest(TestCase):
    prefix = "/api/operations/"

    def setUp(self):
        self.account = Account.objects.create(
            name="Test Account",
            balance=1000
        )
        self.category = Category.objects.create(
            name="Test Category",
            type=Type.EXPENSE,
            is_default=False
        )
        self.operation = Operation.objects.create(
            type=Type.EXPENSE,
            amount=100,
            account=self.account,
            category=self.category,
            description="Test Operation",
            date=datetime.datetime.now()
        )
        self.client = APIClient()

    def test_get_operations(self):
        response = self.client.get(self.prefix)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_operation_expense(self):
        data = {
            "account": self.account.id,
            "amount": 300,
            "type": Type.EXPENSE,
            "category": self.category.id,
            "description": "New Operation"
        }
        response = self.client.post(self.prefix, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Operation.objects.count(), 2)
        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, 600)

    def test_create_operation_income(self):
        data = {
            "account": self.account.id,
            "amount": 300,
            "type": Type.INCOME,
            "category": self.category.id,
            "description": "New Operation"
        }
        response = self.client.post(self.prefix, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Operation.objects.count(), 1)

    def test_update_operation(self):
        data = {
            "account": self.account.id,
            "amount": 200,
            "type": Type.EXPENSE,
            "category": self.category.id,
            "description": "Updated Operation"
        }
        response = self.client.put("{}{}/".format(self.prefix, self.operation.id), data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, 800)

    def test_delete_operation(self):
        response = self.client.delete("{}{}/".format(self.prefix, self.operation.id))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Operation.objects.count(), 0)
