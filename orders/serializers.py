from rest_framework import serializers
from .models import MenuItem, Order, OrderItem
from home.models import MenuCategory
from django.contrib.auth.models import User
from utils.validation_utils import validate_email_address

class MenuItemSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=MenuCategory.objects.all(), source='category',
        write_only=True, required=False
    )
    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'description', 'price','is_available','category_id', 'category_name']

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be a positive number.")
        return value

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Name cannot be empty.")
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Name must be at least 2 characters long.")
        return value.strip()
        
class OrderItemSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    status_name = serializers.CharField(source='status.name', read_only=True)

    class Meta:
        model = Order
        fields = ['id','created_at','total_amount','status_name','items']
        
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        extra_kwargs = {
            'email' : {'required': True},
        }

    def validate_email(self, value):
        is_valid, message = validate_email_address(value)
        if not is_valid:
            raise serializers.ValidationError(message)
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(email=value).exits():
            raise serializers.ValidationError("This email is already in use.")
        return value

    def validate_first_name(self, value):
        if value and not value.strip():
            raise serializers.ValidationError("First name cannot be empty.")
        return value.strip() if value else value
    
    def validate_last_name(self, value):
        if value and not value.strip():
            raise serializers.ValidationError("Last name cannot be empty.")
        return value.strip() if value else value