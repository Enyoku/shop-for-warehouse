from django.contrib.auth.models import User
from django.db import models

from product.models import Product


class OrderStatus(models.TextChoices):
    PROCESSING = 'Processing'
    SHIPPED = 'Shipped'
    DELIVERED = 'Delivered'


class PaymentStatus(models.TextChoices):
    PAID = 'PAID'
    UNPAID = 'UNPAID'


class Order(models.Model):
    total_price = models.DecimalField(max_digits=7, decimal_places=2, blank=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    order_status = models.CharField(
        max_length=50,
        choices=OrderStatus.choices,
        default=OrderStatus.PROCESSING
    )
    payment_status = models.CharField(
        max_length=40,
        choices=PaymentStatus.choices,
        default=PaymentStatus.UNPAID
    )
    delivery_address = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return f"{self.id} | {self.order_status}"


class OrderList(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, related_name="orderlistitems")
    amount = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=7, decimal_places=2, blank=False)

    def __str__(self):
        return f"{self.product} | {self.order}"
