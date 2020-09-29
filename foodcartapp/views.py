from django.templatetags.static import static
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
import json

from .models import Product, Order, OrderProduct
from .serializers import CreateOrderSerializer


def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ], safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def product_list_api(request):
    products = Product.objects.select_related('category').available()

    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'ingridients': product.ingridients,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            },
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return JsonResponse(dumped_products, safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def register_order(request):
    try:
        data = json.loads(request.body.decode())
    except ValueError:
        return JsonResponse({
            'error': 'Failed to decode order!',
        })
    products = [(Product.objects.get(pk=product['product']), product['quantity']) for product in data['products']]
    new_order = Order.objects.create(
        first_name=data['firstname'],
        last_name=data['lastname'],
        phone_number=data['phonenumber'],
        address=data['address'],
    )
    for product, quantity in products:
        OrderProduct.objects.create(
            order=new_order,
            product=product,
            quantity=quantity,
        )
    return JsonResponse({})


class api_register_order(APIView):

    def post(self, request):
        # data = request.data
        # try:
        #     products = data['products']
        #     if not isinstance(products[0]['product'], int):
        #         return Response({'Type Error': 'something wrong with products'}, status=status.HTTP_400_BAD_REQUEST)
        #     for key in data:
        #         if key != 'product':
        #             if not isinstance(data[key], str) or len(data[key]) < 2:
        #                 return Response({'Error': 'something wrong with personal info'}, status=status.HTTP_400_BAD_REQUEST)
        # except (TypeError, IndexError, KeyError):
        #     return Response({'Type Error': 'something wrong with products'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            #...потом переименую
            order_data = {
                "products": request.data['products'],
                "first_name": request.data['firstname'],
                "last_name": request.data['lastname'],
                "phone_number": request.data['phonenumber'],
                "address": request.data['address'],
            }
        except KeyError:
            return Response({'Key Error': 'some fields are missing :('}, status=status.HTTP_400_BAD_REQUEST)
        serializer = CreateOrderSerializer(data=order_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print(serializer.data)
        return JsonResponse({})
