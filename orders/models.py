from django.db import models

class Coupon(models.Model):
    code = models.CharField(max_length=20, unique=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.code
    
class OrderStatus(models.Model):
    """
    Model to represent different order statuses.
    """
    name = models.CharField(max_length=50, unique=True)
    
    class Meta:
        verbose_name = "Order Status"
        verbose_name_plural = "Order Statuses"
    
    def __str__(self):
        return self.name

PENDING = 'Pending'
PROCESSING = 'Processing'
COMPLETED = 'Completed'
CANCELLED = 'Cancelled'