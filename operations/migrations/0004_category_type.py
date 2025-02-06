# Generated by Django 5.1.6 on 2025-02-06 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0003_rename_amount_account_balance'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='type',
            field=models.CharField(choices=[('expense', 'Expense'), ('income', 'Income')], default=1, max_length=7),
            preserve_default=False,
        ),
    ]
