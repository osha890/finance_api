from django.db.models import Model, QuerySet
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware, get_current_timezone
from rest_framework.response import Response

from .models import Type


def get_queryset_for_user(user, model: Model) -> QuerySet:
    queryset = model.objects.all()
    if not user.is_staff:
        queryset = queryset.filter(user=user)
    return queryset


def set_tz(date):
    date = parse_datetime(date)
    if date and date.tzinfo is None:
        date = make_aware(date, get_current_timezone())
    return date


def get_total_amount(queryset):
    total_amount = 0
    for operation in queryset:
        if operation.type == Type.EXPENSE:
            total_amount -= operation.amount
        elif operation.type == Type.INCOME:
            total_amount += operation.amount
        else:
            pass
    return total_amount


def create_response_with_total_amount(queryset, serializer):
    if queryset:
        total_amount = get_total_amount(queryset)
        return Response({
            'total_amount': total_amount,
            'operations': serializer.data
        })
    return Response([])
