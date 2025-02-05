from django.db import models


# Create your models here.


class Type(models.TextChoices):
    EXPENSE = 'expense', 'Expense'
    INCOME = 'income', 'Income'


class Account(models.Model):
    name = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)


class Category(models.Model):
    name = models.CharField(max_length=50)


class Operation(models.Model):
    type = models.CharField(max_length=7, choices=Type.choices)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    account = models.ForeignKey(Account, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    description = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
