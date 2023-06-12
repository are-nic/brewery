from rest_framework import viewsets
from .serializers import ItemSerializer
from .models import Item
from rest_framework.permissions import IsAdminUser


class ItemViewSet(viewsets.ModelViewSet):
    """
    All methods are available for Admins.
    """
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAdminUser]