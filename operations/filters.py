import django_filters

from .models import Operation


class OperationFilter(django_filters.FilterSet):
    type = django_filters.CharFilter(field_name='type', lookup_expr='iexact')
    # date = django_filters.DateFilter(field_name='date', lookup_expr='date')
    date = django_filters.IsoDateTimeFilter(field_name='date', lookup_expr='date')
    date_after = django_filters.IsoDateTimeFilter(field_name='date', lookup_expr='gte')
    date_before = django_filters.IsoDateTimeFilter(field_name='date', lookup_expr='lte')
    account = django_filters.NumberFilter(field_name='account__id')
    category = django_filters.NumberFilter(field_name='category__id')

    class Meta:
        model = Operation
        fields = ['type', 'account', 'category', 'date']
