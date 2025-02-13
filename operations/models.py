from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.contrib.auth import get_user_model

from . import messages

# Create your models here.

User = get_user_model()


class Type(models.TextChoices):
    EXPENSE = 'expense', 'Expense'
    INCOME = 'income', 'Income'


class Account(models.Model):
    name = models.CharField(max_length=50, unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    type = models.CharField(max_length=7, choices=Type.choices)
    is_default = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}: {self.type}"


class Operation(models.Model):
    type = models.CharField(max_length=7, choices=Type.choices)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    account = models.ForeignKey(Account, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    description = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.type}: {self.amount} (date: {self.date})"

    def clean(self):
        if self.category.type != self.type:
            raise ValidationError(messages.WRONG_CATEGORY.format(category=self.category))

    def update_balance(self):
        old_operation = Operation.objects.get(pk=self.pk)
        old_amount = old_operation.amount

        if old_operation.type == Type.INCOME:
            old_amount *= -1

        old_operation.account.balance += old_amount
        old_operation.account.save()

    def save(self, *args, **kwargs):
        self.clean()
        is_new = self.pk is None

        if not is_new:
            self.update_balance()

        with transaction.atomic():
            super().save(*args, **kwargs)
            self.account.refresh_from_db()
            amount = self.amount

            if self.type == Type.EXPENSE:
                amount *= -1

            self.account.balance += amount
            self.account.save()

    def delete(self, *args, **kwargs):
        self.update_balance()
        super().delete(*args, **kwargs)
