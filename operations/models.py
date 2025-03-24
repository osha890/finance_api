from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.contrib.auth import get_user_model

from . import messages

# Create your models here.

User = get_user_model()


class Type(models.TextChoices):
    """Определение типов транзакций (расход и доход)"""
    EXPENSE = 'expense', 'Expense'
    INCOME = 'income', 'Income'


class Account(models.Model):
    name = models.CharField(max_length=50)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        """Ограничение, чтобы у пользователя е повторялись счета"""
        constraints = [
            models.UniqueConstraint(fields=['user', 'name'], name='unique_account_name_per_user')
        ]

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=7, choices=Type.choices)
    is_default = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        """Ограничение, чтобы у пользователя е повторялись категории"""
        constraints = [
            models.UniqueConstraint(fields=['user', 'name'], name='unique_category_name_per_user')
        ]

    def get_default_category(self):
        """Получаем дефолтную категорию по типу"""
        return Category.objects.filter(user=self.user, type=self.type, is_default=True).first()

    def delete(self, *args, **kwargs):
        """Переопределение метода удаления, чтобы при удалении категории переназначить операции"""
        default_category = self.get_default_category()
        if default_category and not self.is_default:
            with transaction.atomic():
                # Переназначаем все операции с этой категорией на категорию по умолчанию
                Operation.objects.filter(category=self).update(category=default_category)
                super().delete(*args, **kwargs)

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
        """Проверка, что тип категории соответствует типу операции (расход или доход)"""
        if self.category.type != self.type:
            raise ValidationError(messages.WRONG_CATEGORY.format(category=self.category))

    def update_balance(self):
        """Возвращаем баланс до операции"""
        operation = Operation.objects.get(pk=self.pk)
        amount = operation.amount

        if operation.type == Type.INCOME:
            amount *= -1

        operation.account.balance += amount
        operation.account.save()

    def save(self, *args, **kwargs):
        self.clean()    # Выполняем проверку на корректность категории
        is_new = self.pk is None    # Проверка, новая ли операция или редактируется существующая

        if not is_new:  # Обновляем баланс, если операция не новая
            self.update_balance()

        with transaction.atomic():
            super().save(*args, **kwargs)   # Сохраняем операцию в базе данных
            self.account.refresh_from_db()  # Обновляем информацию о счете из базы данных
            amount = self.amount

            if self.type == Type.EXPENSE:
                amount *= -1

            self.account.balance += amount
            self.account.save()

    def delete(self, *args, **kwargs):
        """Переопределение метода удаления операции, чтобы обновить баланс счета при удалении"""
        self.update_balance()
        super().delete(*args, **kwargs)
