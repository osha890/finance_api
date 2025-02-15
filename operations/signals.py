from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Category, Type
from . import messages

User = get_user_model()


@receiver(post_save, sender=User)
def create_default_categories(sender, instance, created, **kwargs):
    if created:
        Category.objects.create(name=messages.DEFAULT_CATEGORY_EXPENSE,
                                type=Type.EXPENSE,
                                is_default=True,
                                user=instance)

        Category.objects.create(name=messages.DEFAULT_CATEGORY_INCOME,
                                type=Type.INCOME,
                                is_default=True,
                                user=instance)
