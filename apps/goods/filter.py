import django_filters
from .models import Goods


class GoodsFilter(django_filters.rest_framework.FilterSet):
    prick_min = django_filters.NumberFilter(field_name='shop_price', lookup_expr='gt')
    prick_max = django_filters.NumberFilter(field_name='shop_price', lookup_expr='lt')

    class Meta:
        model = Goods
        fields = ['prick_min', 'prick_max']
