from django import forms
from django.shortcuts import redirect, render
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test

from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views
from restaurateur.services import find_restaurant


from foodcartapp.models import Product, Restaurant, Order, RestaurantMenuItem


class Login(forms.Form):
    username = forms.CharField(
        label='Логин', max_length=75, required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Укажите имя пользователя'
        })
    )
    password = forms.CharField(
        label='Пароль', max_length=75, required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )


class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = Login()
        return render(request, "login.html", context={
            'form': form
        })

    def post(self, request):
        form = Login(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                if user.is_staff:  # FIXME replace with specific permission
                    return redirect("restaurateur:RestaurantView")
                return redirect("start_page")

        return render(request, "login.html", context={
            'form': form,
            'ivalid': True,
        })


class LogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('restaurateur:login')


def is_manager(user):
    return user.is_staff  # FIXME replace with specific permission


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_products(request):
    restaurants = list(Restaurant.objects.order_by('name'))
    products = list(Product.objects.prefetch_related('menu_items'))

    default_availability = {restaurant.id: False for restaurant in restaurants}
    products_with_restaurants = []
    for product in products:

        availability = {
            **default_availability,
            **{item.restaurant_id: item.availability for item in product.menu_items.all()},
        }
        orderer_availability = [availability[restaurant.id] for restaurant in restaurants]

        products_with_restaurants.append(
            (product, orderer_availability)
        )

    return render(request, template_name="products_list.html", context={
        'products_with_restaurants': products_with_restaurants,
        'restaurants': restaurants,
    })


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_restaurants(request):
    return render(request, template_name="restaurants_list.html", context={
        'restaurants': Restaurant.objects.all(),
    })


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_orders(request):
    orders = Order.objects.all().prefetch_related('order_products__product')
    restaurants = Restaurant.objects.all().prefetch_related('menu_items__product')
    restaurants_and_items = [(restaurant.name, [menu_item.product.name for menu_item in restaurant.menu_items.all() if
                                            menu_item.availability]) for restaurant in restaurants]

    orders_info = []
    for order in orders:
        order_items = [product.product.name for product in order.order_products.all()]
        print(find_restaurant(restaurants_and_items, order_items))
        order_info = {
            'id': order.id,
            'status': order.get_order_status_display(),
            'payment_method': order.get_payment_method_display(),
            'cart_total': order.cart_total['cart_total'],
            'name': order.firstname + ' ' + order.lastname,
            'phone': order.phone_number_pure,
            'address': order.address,
            'comment': order.comment,
            'restaurants': find_restaurant(restaurants_and_items, order_items),
        }
        # property cart total содаёт кучу запросов, а как их убрать пока хз
        orders_info.append(order_info)


    # for order in orders:
    # print([[menu_item.restaurant.name for menu_item in product.product.menu_items.all().prefetch_related('restaurant')] for product in order.order_products.all().prefetch_related('product')])

    # menu_items = RestaurantMenuItem.objects.all().prefetch_related('restaurant_name').prefetch_related('product_id')
    print(restaurants_and_items)
    return render(request, template_name='order_items.html', context={
        'orders': orders_info,
    })
