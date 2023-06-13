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

    def create(self, request, *args, **kwargs):
        """ Override method fom POST order """
        items_data = request.data.get('items')
        order_items = []
        if items_data:
            for item_data in items_data:                                    # перебираем все товары заказа из тела запроса
                item_id = item_data.get('item')                             # получаем id Товара, который хотим заказать
                order_item_qty = item_data.get('qty')                       # получаем кол-во, которое необходимо заказать
                max_qty = item_data.get('max_qty')                          # получаем значение поля "Максимальное кол-во"

                if item_id:                                                 # если переданы в теле запроса id товара со склада

                    if order_item_qty and order_item_qty > 0:               # если передано в теле запроса кол-во товара и оно больше 0
                        try:
                            item = Item.objects.get(pk=item_id)             # получаем экземпляр Товара
                            if item.qty >= order_item_qty:                  # если кол-во запрашиваемого товара меньше либо равно кол-ву Товара на складе
                                order_items.append(OrderItem(item=item, qty=order_item_qty))
                                item.qty -= order_item_qty                  # уменьшаем кол-во Товара на складе
                                item.save()                                 # сохраняем изменения в Товаре
                            else:
                                return Response({'error': f"Not enough quantity available for item: {item.name}"}, status=status.HTTP_400_BAD_REQUEST)
                        except Item.DoesNotExist:
                            return Response({'error': f"Item with id {item_id} does not exist"}, status=status.HTTP_400_BAD_REQUEST)

                    elif max_qty:                                           # если в теле запроса передам параметр "max_qty" и он True
                        try:
                            item = Item.objects.get(pk=item_id)             # получаем экземпляр Товара
                            if item.qty > 0:                                # если кол-во запрашиваемого товара больше 0
                                order_items.append(OrderItem(item=item, qty=item.qty))
                                item.qty = 0                                # уменьшаем кол-во Товара на складе до 0
                                item.save()                                 # сохраняем изменения в Товаре
                            else:
                                return Response({'error': f"Not enough quantity available for item: {item.name}"}, status=status.HTTP_400_BAD_REQUEST)
                        except Item.DoesNotExist:
                            return Response({'error': f"Item with id {item_id} does not exist"}, status=status.HTTP_400_BAD_REQUEST)

            if len(order_items) > 0:                                        # если в списке Товаров заказа есть экземпляры
                order = Order.objects.create(customer=self.request.user)    # создаем экземпляр заказа
                for order_item in order_items:                              # перебираем все Товары заказа из списка
                    order_item.order = order                                # присваиваем им заказ, к которому они принадлежат
                    order_item.save()                                       # сохраняем Товары заказа в БД
            else:
                return Response({'error': "Not enough data to create Order"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'Order complete - order_id': order.id}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': "No items provided"}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        order_data = request.data                                                   # Получить данные из запроса
        order_items_data = order_data.pop('items', [])
        order = Order.objects.get(id=kwargs['pk'])                                  # Получить экземпляр заказа из БД
        print()

        if order_items_data:
            for item_data in order_items_data:                                      # перебираем все товары заказа из тела запроса
                item_id = item_data.get('item')                                     # получаем id Товара, который хотим заказать
                max_qty = item_data.get('max_qty')                                  # получаем значение поля "Максимальное кол-во"

                if max_qty:                                                         # Если поле 'max_qty' равно True, выполнить логику обновления Заказа
                    try:
                        item = Item.objects.get(id=item_id)                         # получаем экземпляр Товара
                        if item.qty > 0:                                            # если кол-во запрашиваемого товара больше 0
                            OrderItem.objects.create(order=order, item=item, qty=item.qty)
                            item.qty = 0                                            # уменьшаем кол-во Товара на складе до 0
                            item.save()                                             # сохраняем изменения в Товаре
                        else:
                            return Response({'error': f"Not enough quantity available for item: {item.name}"}, status=status.HTTP_400_BAD_REQUEST)
                    except Item.DoesNotExist:
                        return Response({'error': f"Item with id {item_id} does not exist"}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    super().update(request, *args, **kwargs)                        # Если поле 'max_qty' не равно True, выполнить стандартное обновление

            # Сериализовать и вернуть созданный заказ
            serializer = self.get_serializer(order)
            return Response(serializer.data)

        return Response({'error': "No items provided"}, status=status.HTTP_400_BAD_REQUEST)


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


