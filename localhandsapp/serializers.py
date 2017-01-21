from rest_framework import serializers

# from localhandsapp.models import Scooper, Task
from localhandsapp.models import Scooper, \
    Task, \
    Customer, \
    Driver, \
    Order, \
    OrderDetails

class ScooperSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()

    def get_logo(self, scooper):
        request = self.context.get('request')
        logo_url = scooper.logo.url
        return request.build_absolute_uri(logo_url)

    class Meta:
        model = Scooper
        fields = ("id", "name", "phone", "address", "logo")


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ("id", "name", "short_description", "price")


# ORDER SERIALIZER
class OrderCustomerSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source="user.get_full_name")

    class Meta:
        model = Customer
        fields = ("id", "name", "avatar", "phone", "address")

class OrderDriverSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source="user.get_full_name")

    class Meta:
        model = Driver
        fields = ("id", "name", "avatar", "phone", "address")

class OrderScooperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scooper
        fields = ("id", "name", "phone", "address")

class OrderTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ("id", "name", "price")

class OrderDetailsSerializer(serializers.ModelSerializer):
    task = OrderTaskSerializer()

    class Meta:
        model = OrderDetails
        fields = ("id", "task", "quantity", "sub_total")

class OrderSerializer(serializers.ModelSerializer):
    customer = OrderCustomerSerializer()
    driver = OrderDriverSerializer()
    scooper = OrderScooperSerializer()
    order_details = OrderDetailsSerializer(many = True)
    status = serializers.ReadOnlyField(source = "get_status_display")

    class Meta:
        model = Order
        fields = ("id", "customer", "scooper", "driver", "order_details", "total", "status", "address")
