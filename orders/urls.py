from django.urls import path, include
from .views import MenuItemSearchViewSet, OrderHistoryView, UpdateEmailView, MenuItemUpdateViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'api/menu-items/search', MenuItemSearchViewSet, basename='menu-item-search')
router.register(r'api/menu-items', MenuItemUpdateViewSet, basename='menu-item-update')
urlpatterns = [
    path('api/', include(router.urls)),
    path('api/order-history/', OrderHistoryView.as_view(), name='order_history'),
    path('api/update-email/', UpdateEmailView.as_view(), name='update_email'),
]