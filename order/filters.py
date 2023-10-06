from django_filters import rest_framework as filters

from order.models import Order


class OrderFilters(filters.FilterSet):
    class Meta:
        model = Order
        fields = ('id', 'order_status', 'payment_status')
