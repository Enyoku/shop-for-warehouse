from django.contrib.auth.models import User
from rest_framework import serializers

from order.models import Order, OrderList
from account.serializers import ClientSerializer


class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderList
        fields = "__all__"


class OrderCreateSerializer(serializers.ModelSerializer):
    orderList = serializers.SerializerMethodField(method_name='get_order_list', read_only=True)
    user = serializers.SerializerMethodField(method_name="get_user_credentials", read_only=True)
    class Meta:
        model = Order
        fields = "__all__"

    def get_order_list(self, obj):
        order_list = obj.orderlistitems.all()
        serializer = OrderListSerializer(order_list, many=True)
        return serializer.data
    
    def get_user_credentials(self, obj):
        user = obj.user
        serializer = ClientSerializer(user, many=False)
        return serializer.data
