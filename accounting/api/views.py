from rest_framework import viewsets
from .serializers import OrderItemSerializer
from .models import OrderItem
from rest_framework.permissions import IsAdminUser


class OrderItemViewSet(viewsets.ReadOnlyModelViewSet):
    """
    GET method are available for Admins.
    """
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAdminUser]