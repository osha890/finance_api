from django.contrib import admin

from .models import Account, Category, Operation


# Register your models here.

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'balance', 'user')
    list_display_links = ('id', 'name')
    list_filter = ('user',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type', 'user')
    list_display_links = ('id', 'name')
    list_filter = ('type', 'user')


@admin.register(Operation)
class OperationAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'amount', 'account', 'category', 'date', 'user')
    list_display_links = ('id', 'type')
    list_filter = ('type', 'account', 'category', 'user')
