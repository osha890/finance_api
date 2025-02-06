from django.contrib import admin
from .models import Account, Category, Operation


# Register your models here.

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'balance')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Operation)
class OperationAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'amount', 'account', 'category', 'date')
    list_display_links = ('id', 'type')
    list_filter = ('type', 'account', 'category')

