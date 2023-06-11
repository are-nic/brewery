from rest_framework import viewsets
from .models import *
from .serializers import OrderListSerializer, OrderDetailSerializer, OrderItemSerializer
from .permissions import CustomerOrderOrReadOnly
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated

User = get_user_model()


# ---------------------------------------------For Nested Routers--------------------------------------------
class OrderViewSet(viewsets.ModelViewSet):
    """
    Создан для вложенных маршрутов, связанных с Заказом
    Все методы для работы с заказами.
    Доступ: создание заказа для любого аутентифицированного юзера
            действия над заказами доступны для владельцев заказа или суперпользователю
    """

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [CustomerOrderOrReadOnly]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Order.objects.all()
        else:
            return Order.objects.filter(customer=self.request.user.id)

    def get_serializer_class(self):
        """Выбор сериализатора в зависимости от применяемого метода"""
        if self.action == 'list':
            return OrderListSerializer
        return OrderDetailSerializer

    def perform_create(self, serializer):
        """При создании заказа текущий юзер заносится в поле Customer"""
        items = self.request.data.pop('items')

        order = Order.objects.create(
            customer=self.request.user,
            pay_method=self.request.data.get('pay_method'),
        )

        for item_data in items:
            item = Item.objects.filter(title=item_data.get('item')).first()
            OrderItem.objects.create(
                item=item,
                qty=item_data.get('qty'),
                order=order
            )


class OrderItemViewSet(viewsets.ModelViewSet):
    """
    Создан для вложенных маршрутов, связанных с Заказом
    Для взаимодействия с продуктами заказа
    get, post, put, patch, delete
    """
    serializer_class = OrderItemSerializer

    def get_queryset(self):
        return OrderItem.objects.filter(order=self.kwargs['orders_pk'])
# ----------------------------------------------------------------------------------------------------------


class OrderItemDetailView(viewsets.ModelViewSet):
    """
    Конечная точка API, позволяющая просматривать, создавать или редактировать продукты заказа.
    get, post, put, patch, delete
    сортировка по заказам
    доступ: Ко всем продуктам заказов в БД имеет доступ Суперпользователь
            Любой пользователь имеет доступ к своим продуктам заказа.
    """
    queryset = OrderItem.objects.order_by('order')
    serializer_class = OrderItemSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset
        return self.queryset.filter(order__customer=self.request.user)
