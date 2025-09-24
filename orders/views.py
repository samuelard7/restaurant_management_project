from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from .models import MenuItem
from .serializers import MenuItemSerializer

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10  # Number of items per page
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

    def get_queryset(self):
        """
        Filter menu items based on the 'search' query parameter.
        """
        queryset = super().get_queryset()
        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
        return queryset.order_by('name')


