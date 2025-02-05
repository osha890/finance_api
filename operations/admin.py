from django.contrib import admin
from .models import Account, Category, Operation


# Register your models here.

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Operation)
class OperationAdmin(admin.ModelAdmin):
    pass
