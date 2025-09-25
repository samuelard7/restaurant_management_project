from django.db import models
from django.contrib.auth.models import User
from home.models import MenuCategory

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(MenuCategory, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Menu Item"
        verbose_name_plural = "Menu Items"

class Coupon(models.Model):
    code = models.CharField(max_length=20, unique=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.code

class OrderStatus(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Order Status"
        verbose_name_plural = "Order Statuses"

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.ForeignKey(OrderStatus, on_delete=models.SET_NULL, null=True, related_name='orders')

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"
        
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price at time of order

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name if self.menu_item else 'Deleted Item'}"

    class Meta:
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"


PENDING = 'Pending'
PROCESSING = 'Processing'
COMPLETED = 'Completed'
CANCELLED = 'Cancelled'