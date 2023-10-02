from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from order.models import Order, OrderList
from order.serializers import OrderListSerializer, OrderSerializer
from order.filters import OrderFilters
from product.models import Product


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def new_order(request):
    data = request.data
    user = request.user

    order_list = data['orderList']

    if order_list and len(order_list) == 0:
        return Response({"error": "No order items. Please add at least one product"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        for item in order_list:
            item['price'] = Product.objects.get(id=item['product']).price
        total_amount = sum(item['price'] * item['amount'] for item in order_list)

        order = Order.objects.create(
            total_price=total_amount,
            user=user,
            order_status=data['order_status'],
            payment_status=data['payment_status'],
            delivery_address=data['delivery_address']
        )

        for i in order_list:
            product = Product.objects.get(id=i['product'])

            item = OrderList.objects.create(
                product=product,
                order=order,
                amount=i['amount'],
                price=i['price']
            )

            # Update product amount
            product.amount -= item.amount
            product.save()

        serializer = OrderCreateSerializer(order, many=False)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_orders(request):
    user = get_object_or_404(User, email=request.user)
    filterset = OrderFilters(
        request.GET,
        queryset=Order.objects.filter(user=user.pk).order_by("id")
    )

    count = filterset.qs.count()

    # Pagination
    resPerPage = 3

    paginator = PageNumberPagination()
    paginator.page_size = resPerPage
    queryset = paginator.paginate_queryset(filterset.qs, request)

    serializer = OrderSerializer(queryset, many=True)
    return Response({
        'resPerPage': resPerPage,
        'count': count,
        'orders': serializer.data
    })


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def process_order(request, id):
    data = request.data
    order = get_object_or_404(Order, id=id)

    order.order_status = data['order_status']
    order.save()

    serializer = OrderSerializer(order, many=False)
    return Response({'order': serializer.data})
