from rest_framework import viewsets
from .serializers import ItemSerializer
from .models import Item
from rest_framework.permissions import IsAdminUser, IsAuthenticated


class ItemViewSet(viewsets.ModelViewSet):
    """
    GET method is available for Authenticated users. All methods are available for Admins.
    """
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]