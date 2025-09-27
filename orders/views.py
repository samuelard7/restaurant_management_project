from rest_framework import viewsets, generics
from django.shortcuts import render
from .forms import UserProfileForm
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from rest_framework.exceptions import NotFound, ValidationError
from django.core.exceptions import ObjectDoesNotExist
from .models import MenuItem, Order
from utils.validation_utils import validate_email_address
from .serializers import MenuItemSerializer, OrderSerializer, UserProfileSerializer
from rest_framework.response import Response
from django.contrib.auth.models import User

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


class UpdateEmailView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        form = UserProfileForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            request.user.email = email
            request.user.save()
            return JsonResponse({"status":"success", "message":"Email updated successfully"})
        else:
            return JsonResponse({"status":"error", "message":form.errors}, status=400)



class MenuItemUpdateViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAdminUser]
    http_method_names = ['put', 'options']

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            raise NotFound("Menu item not found.")
        except ValidationError as e:
            return Response({"detail": str(e)}, status=400)
        except Exception as e:
            return Response({"detail": "An unexpected error occurred."}, status=500)


class UserProfileViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    http_method_names = ['put', 'get', 'options']

    def retrieve(self, request, *args, **kwargs):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        try:
            serializer = UserProfileSerializer(
                request.user,
                data = request.data,
                partial=True,
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except ValidationError as e:
            return Response({"detail": str(e)}, status=400)
        except Exception as e:
            return Response({
                "detail": "Anunexpected error occured."
            }, status = 500)
            