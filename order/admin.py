from django.contrib import admin

from order.models import Order, OrderList


admin.site.register(Order)
admin.site.register(OrderList)
