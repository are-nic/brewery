from rest_framework import viewsets, status, mixins
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from .models import *
from .serializers import *
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated, AllowAny

User = get_user_model()


class RegisterUserView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['response'] = "You've been registered"
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = serializer.errors
            return Response(data)


# --------------------------------------------- ORDERS --------------------------------------------
class OrderViewSet(viewsets.ModelViewSet):
    """
    Methods for orders
    Access: POST order is available from IsAuthenticated users
            GET, PUT, PATCH, DELETE are available for order's owner or Superuser
    """
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Order.objects.all()
        else:
            return Order.objects.filter(customer=self.request.user.id)

    def get_serializer_class(self):
        """ Choice of serializer depends on the method """
        if self.action == 'list':
            return OrderListSerializer
        return OrderDetailSerializer

    def perform_create(self, serializer):
        """ When Order created the current user saves as a customer """
        items = self.request.data.pop('items')

        order = Order.objects.create(customer=self.request.user)

        for item_data in items:
            item = Item.objects.filter(id=item_data.get('item')).first()
            OrderItem.objects.create(
                item=item,
                qty=item_data.get('qty'),
                order=order
            )


# ----------------------------------------- ITEM -----------------------------------
class ItemViewSet(mixins.ListModelMixin,
               mixins.RetrieveModelMixin,
               viewsets.GenericViewSet):
    """
    GET methods are available for Authenticated Users.
    """
    queryset = Item.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ItemSerializer


