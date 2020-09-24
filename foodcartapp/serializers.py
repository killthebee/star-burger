from rest_framework import serializers

from .models import Order, OrderProduct, Product


class CreateOrderSerializer(serializers.ModelSerializer):

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
