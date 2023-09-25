from django_filters import rest_framework as filters

from product.models import Product


class ProductFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    firm = filters.CharFilter(field_name='firm', lookup_expr='icontains')

    min_price = filters.NumberFilter(field_name='price' or 0, lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price' or 1000000, lookup_expr='lte')

    class Meta:
        model = Product
        fields = ('name', 'firm', 'min_price', 'max_price', 'in_stock', 'category')
