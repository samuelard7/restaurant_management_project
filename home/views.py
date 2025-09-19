from rest_framework import generics
from .models import MenuCategory
from .serializers import MenuCategorySerializer

class MenuCategoryListView(generics.ListAPIView):
    queryset = MenuCategory.objects.all()
    serializer_class = MenuCategorySerializer