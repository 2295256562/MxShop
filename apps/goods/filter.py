import django_filters
from goods.models import Goods
from django.db.models import Q


class GoodsFilter(django_filters.rest_framework.FilterSet):
    pricemin = django_filters.NumberFilter(field_name='shop_price', lookup_expr='gt')
    pricemax = django_filters.NumberFilter(field_name='shop_price', lookup_expr='lt')
    top_category = django_filters.NumberFilter(method='top_category_filter')

    def top_category_filter(self, queryset, name, value):
        return queryset.filter(Q(category_id=value) | Q(category__parent_category_id=value) | Q(
            category__parent_category__parent_category_id=value))

    class Meta:
        model = Goods
        fields = ['pricemin', 'pricemax']
