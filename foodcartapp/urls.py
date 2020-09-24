from django.urls import path

from .views import product_list_api, banners_list_api, register_order, api_register_order


app_name = "foodcartapp"

urlpatterns = [
    path('products/', product_list_api),
    path('banners/', banners_list_api),
    path('order/', api_register_order.as_view()),
]
