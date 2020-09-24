from django.templatetags.static import static
from django.http import JsonResponse
from rest_framework.views import APIView
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
        data = request.data
        products = data['products']
        order_data = {
            "first_name":data['firstname'],
            "last_name":data['lastname'],
            "phone_number":data['phonenumber'],
            "address":data['address'],
        }
        serializer = CreateOrderSerializer(data=order_data)
        if serializer.is_valid():
            serializer.save(products=products)
            return Response(status=201)
        else:
            return Response(status=400)
