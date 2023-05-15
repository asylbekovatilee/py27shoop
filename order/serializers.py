from rest_framework.serializers import ModelSerializer,OrderItemSerializer
from drf_writable_nested import WritableNestedModelSerializer

from .models import Order, OrderItem

class OrderItem(ModelSerializer):
    class Meta:
        model = OrderItem
        exclude = ("order")

class OrderSerializer(WritableNestedModelSerializer, ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ("user", "is_paid", "created_at", "total_price", "items")
