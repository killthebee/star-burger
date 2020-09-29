from rest_framework import serializers

from .models import Order, OrderProduct, Product


class ProductSerializer(serializers.Serializer):
    product = serializers.IntegerField(required=True)
    quantity = serializers.IntegerField(required=True)

    def validate_product(self, value):
        if not value:
            raise serializers.ValidationError('No product')
        else:
            return value

    def validate_quantity(self, value):
        if not value:
            raise serializers.ValidationError('No product quantity')
        else:
            return value


class CreateOrderSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, allow_empty=False)

    class Meta:
        model = Order
        exclude = ['phone_number_pure']

    def create(self, validated_data):
        products = [(Product.objects.get(pk=product['product']), product['quantity']) for product in validated_data.get('products')]
        new_order = Order.objects.create(
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            phone_number=validated_data.get('phone_number'),
            address=validated_data.get('address'),
        )
        for product, quantity in products:
            OrderProduct.objects.create(
                order=new_order,
                product=product,
                quantity=quantity,
            )
        return True
