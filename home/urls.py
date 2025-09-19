from django.urls import path
from .views import MenuCategoryListView

urlpatterns = [
    path('api/menu-categories/', MenuCategoryListView.as_view(), name='menu_category_list'),
]