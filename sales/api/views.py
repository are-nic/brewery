from rest_framework import viewsets, status, mixins
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from .models import *
from .serializers import *
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404

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
    Methods for Orders.
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

    @staticmethod
    def change_item_qty(order_items_list):
        """ When the order is placed, subtract qty from Item instance """
        for order_item in order_items_list:
            item = order_item.item
            item.qty -= order_item.qty
            item.save()

    def create(self, request, *args, **kwargs):
        """ Overrode create method for POST """
        items_data = request.data.get('items', [])
        order_is_placed = request.data.get('is_placed')                 # статус размещения заказа
        order_items = []

        for item_data in items_data:                                    # перебираем все товары заказа из тела запроса
            item_id = item_data.get('item')                             # получаем id Товара, который хотим заказать
            order_item_qty = item_data.get('qty')                       # получаем кол-во, которое необходимо заказать
            max_qty = item_data.get('max_qty')                          # получаем значение поля "Максимальное кол-во"

            try:
                item = get_object_or_404(Item, pk=item_id)       # пробуем получить экземпляр Товара
            except Item.DoesNotExist:
                return Response({'error': f"Item with id {item_id} does not exist"}, status=status.HTTP_400_BAD_REQUEST)

            if order_item_qty and order_item_qty > 0:           # если в теле запроса передано кол-во товара 'qty' и оно > 0
                if item.qty >= order_item_qty:                  # если кол-во запрашиваемого товара <= кол-ву Товара на складе
                    order_items.append(OrderItem(item=item, qty=order_item_qty))
                else:                                           # если кол-во какого-либо из товаров заказа превысило текущее кол-во товара
                    order_items.clear()                         # очищаем список Товаров Заказа
                    return Response({'error': f"Not enough quantity available for item {item.name}"}, status=status.HTTP_400_BAD_REQUEST)

            elif max_qty and not order_item_qty:                # если в теле запроса передан параметр "max_qty" и он True
                if item.qty > 0:                                # если кол-во запрашиваемого товара больше 0
                    order_items.append(OrderItem(item=item, qty=item.qty))
                else:
                    order_items.clear()                         # очищаем список Товаров Заказа
                    return Response({'error': f"Not enough quantity available for item {item.name}"}, status=status.HTTP_400_BAD_REQUEST)

        if len(order_items) > 0:                                        # если в списке Товаров Заказа есть экземпляры
            order = Order.objects.create(                               # создаем экземпляр заказа
                customer=self.request.user,
                is_placed=order_is_placed
            )
            for order_item in order_items:                              # перебираем все Товары заказа из списка
                order_item.order = order                                # присваиваем им Заказ, к которому они относятся
                order_item.save()                                       # сохраняем Товары Заказа в БД

            if order_is_placed:                                         # Если флаг размещения заказа is True
                self.change_item_qty(order_items)

            order_items.clear()

            return Response({'Order complete - order_id': order.id}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': "Not enough data to create Order"}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """ Overrode update method for PUT and PATCH """
        order_data = request.data                                   # Получить данные из запроса
        order = Order.objects.get(id=kwargs['pk'])                  # Получить экземпляр заказа из БД

        if order.is_placed:                                         # если данный заказ уже размещен (is_placed = True), то выдать ошибку обновления
            return Response({'Error': "This Order already was placed. Create another Order"}, status=status.HTTP_400_BAD_REQUEST)

        order_items_data = order_data.pop('items', [])              # получаем данные товаров заказа из тела запроса и проверка на непустой список
        order_is_placed = request.data.get('is_placed')             # статус размещения заказа

        order_items = []

        for item_data in order_items_data:                      # перебираем все товары заказа из тела запроса
            item_id = item_data.get('item')                     # получаем id Товара, который хотим заказать
            max_qty = item_data.get('max_qty')                  # получаем значение поля "Максимальное кол-во" (True or False)
            order_item_qty = item_data.get('qty')               # получаем кол-во, которое необходимо заказать

            try:
                item = get_object_or_404(Item, pk=item_id)       # пробуем получить экземпляр Товара
            except Item.DoesNotExist:
                return Response({'error': f"Item with id {item_id} does not exist"}, status=status.HTTP_400_BAD_REQUEST)

            if order_item_qty and order_item_qty > 0:     # если передано кол-во Товара Заказа и оно > 0
                if item.qty >= order_item_qty:              # если кол-во запрашиваемого товара меньше либо равно кол-ву Товара на складе
                    order_items.append(OrderItem(
                        order=order,
                        item=item,
                        qty=order_item_qty
                    ))
                else:
                    return Response({'error': f"Not enough quantity available for item: {item.name}"}, status=status.HTTP_400_BAD_REQUEST)

            elif max_qty and not order_item_qty:              # Если поле 'max_qty' равно True и нет поля 'qty', выполнить логику обновления Заказа
                if item.qty > 0:                            # если кол-во запрашиваемого товара больше 0
                    order_items.append(OrderItem(
                        order=order,
                        item=item,
                        qty=item.qty
                    ))
                else:
                    return Response({'error': f"Not enough quantity available for item: {item.name}"}, status=status.HTTP_400_BAD_REQUEST)

        if len(order_items) > 0:                                # если в списке Товаров Заказа есть экземпляры
            for order_item in order_items:                      # перебираем все Товары заказа из списка
                OrderItem.objects.update_or_create(             # Обновляем кол-во Товара Заказа, если таковой уже имеется в Заказе, либо создаем новый
                    order=order_item.order,
                    item=order_item.item,
                    defaults={'qty': order_item.qty}
                )
            if order_is_placed:
                order.is_placed = True
                order.save()
                self.change_item_qty(order_items)

        order_items.clear()
        # Сериализовать и вернуть созданный заказ
        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)


# ----------------------------------------- ITEM -----------------------------------
class ItemViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    GET methods are available for Authenticated Users.
    """
    queryset = Item.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ItemSerializer


