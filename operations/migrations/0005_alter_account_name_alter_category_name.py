# Generated by Django 5.1.6 on 2025-02-13 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0004_category_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
