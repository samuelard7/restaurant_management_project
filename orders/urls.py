from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MenuItemSearchViewSet

# Create a router and register the viewset
router = DefaultRouter()
router.register(r'menu-items/search', MenuItemSearchViewSet, basename='menu-item-search')

urlpatterns = [
    path('api/', include(router.urls)),
]