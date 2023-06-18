from rest_framework import serializers
from .models import Order, OrderItem, Item
from django.contrib.auth import get_user_model
from drf_writable_nested import WritableNestedModelSerializer

User = get_user_model()


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    max_qty = serializers.BooleanField(required=False, allow_null=True)

    class Meta:
        model = OrderItem
        fields = ('id', 'item', 'qty', 'max_qty')


class OrderListSerializer(serializers.ModelSerializer):
    """ Orders' list """
    customer = serializers.CharField(source="customer.username", read_only=True)

    class Meta:
        model = Order
        fields = '__all__'


class OrderDetailSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    """ A order's detail """
    customer = serializers.CharField(source="customer.username", read_only=True)
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )
        return user

    class Meta:
        model = User
        fields = ['username', 'password']