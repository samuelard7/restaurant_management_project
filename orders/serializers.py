from rest_framework import serializers
from .models import MenuItem, Order, OrderItem, MenuCategory

class MenuItemSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'description', 'price', 'category_name']

class OrderItemSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    status_name = serializers.CharField(source='status.name', read_only=True)

    class Meta:
        model = Order
        fields = ['id','created_at','total_amount','status_name','items']
        