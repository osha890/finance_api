from django.db import models, transaction


# Create your models here.


class Type(models.TextChoices):
    EXPENSE = 'expense', 'Expense'
    INCOME = 'income', 'Income'


class Account(models.Model):
    name = models.CharField(max_length=50)
    balance = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Operation(models.Model):
    type = models.CharField(max_length=7, choices=Type.choices)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    account = models.ForeignKey(Account, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    description = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type}: {self.amount} (date: {self.date})"

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        if not is_new:
            old_operation = Operation.objects.get(pk=self.pk)
            old_amount = old_operation.amount

            if old_operation.type == Type.INCOME:
                old_amount *= -1

            old_operation.account.balance += old_amount
            old_operation.account.save()

        with transaction.atomic():
            super().save(*args, **kwargs)
            self.account.refresh_from_db()
            amount = self.amount

            if self.type == Type.EXPENSE:
                amount *= -1

            self.account.balance += amount
            self.account.save()
