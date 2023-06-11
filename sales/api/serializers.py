from rest_framework import serializers
from .models import Order, OrderItem


class ChoiceField(serializers.ChoiceField):
    """
    Настраиваемое поле для поля выбора значений
    """
    def to_representation(self, obj):
        # Предоставляет читабельное значение из списка choices полей модели
        if obj == '' and self.allow_blank:
            return obj
        return self._choices[obj]

    def to_internal_value(self, data):
        # Поддерживает отправляемые значения через post, put, patch методы
        if data == '' and self.allow_blank:
            return ''

        for key, val in self._choices.items():
            if val == data:
                return key
        self.fail('invalid_choice', input=data)


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('item', 'qty')


class OrderListSerializer(serializers.ModelSerializer):
    """Список Заказов"""
    customer = serializers.CharField(source="customer.name", read_only=True)
    pay_method = ChoiceField(choices=Order.PAY_METHOD)

    class Meta:
        model = Order
        fields = '__all__'


class OrderDetailSerializer(serializers.ModelSerializer):
    """Один Заказ"""

    customer = serializers.CharField(source="customer.name", read_only=True)
    items = OrderItemSerializer(many=True)
    pay_method = ChoiceField(choices=Order.PAY_METHOD)

    class Meta:
        model = Order
        fields = '__all__'

    def update(self, instance, validated_data):
        """
        Обновление экземпляра товара заказа и самого заказа
        """
        if 'items' in validated_data:
            items_data = validated_data.pop('items')
            items = instance.items.all()
            items = list(items)
            for item_data in items_data:
                item = items.pop(0)
                item.qty = item_data.get('qty', item.qty)
                item.save()

        instance.pay_method = validated_data.get('pay_method', instance.pay_method)
        instance.save()

        return instance