from rest_framework import viewsets, generics
from django.shortcuts import render
from .forms import UserProfileForm
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from .models import MenuItem, Order
from .serializers import MenuItemSerializer, OrderSerializer

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class MenuItemSearchViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint to search menu items by name (case-insensitive).
    Supports ?search=query parameter.
    """
    queryset = MenuItem.objects.all().select_related('category')
    serializer_class = MenuItemSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self, request):
        """
        Filter menu items based on the 'search' query parameter.
        """
        queryset = super().get_queryset()
        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
        return queryset.order_by('name')

class OrderHistoryView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get(self, request):
        orders = Order.objects.filter(user=request.user).select_related('status').prefetch_related('items__menu_item').order_by('-created_at')

        paginator = self.pagination_class()
        paginated_orders = paginator.paginate_queryset(orders, request)

        serializer = OrderSerializer(paginated_orders, many=True)
        return paginator.get_paginated_response(serializer.data)

class MenuItemByCategoryView(generics.ListAPIView):
    serializer_class = MenuItemSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self, request):
        queryset = MenuItem.objects.select_related('category').all()
        category_name = self.request.query_params.get('category', None)
        if category_name:
            queryset = queryset.filter(category__name__iexact=category_name)
        return queryset.order_by('name')
