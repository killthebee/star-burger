import requests
from geopy import distance
from django.core.cache import cache


def fetch_coordinates(apikey, place):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    params = {"geocode": place, "apikey": apikey, "format": "json"}
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    places_found = response.json()['response']['GeoObjectCollection']['featureMember']
    most_relevant = places_found[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lon, lat


def add_distances(restaurants, order_coords):
    for restaurant in restaurants:
        restaurant['delivery_distance'] = round(distance.distance(restaurant['coords'], order_coords).km, 2)
    return restaurants


def find_restaurants(restaurants, order):
    order_coords = cache.get_or_set(f'order_{order.address}', fetch_coordinates('5dc7eb7b-c53a-4e7c-888b-dca7802f59eb', order.address), 120)
    order_items = [product.product.name for product in order.order_products.all()]
    possible_restaurants = []
    for order_item in order_items:
        for restaurant in restaurants:
            if order_item in restaurant['menu_items']:
                possible_restaurants.append(restaurant)

    uniq_possible_restaurants = list({v['name']:v for v in possible_restaurants}.values())
    possible_restaurants = add_distances(uniq_possible_restaurants, order_coords)
    return possible_restaurants


def serialize_restaurants(restaurants):
    serialized_restaurants = []
    for restaurant in restaurants:
        serialized_restaurants.append(
            {
                'name': restaurant.name,
                'menu_items': [menu_item.product.name for menu_item in restaurant.menu_items.all() if menu_item.availability],
                'coords': cache.get_or_set(f'restaurant_{restaurant.id}', fetch_coordinates('5dc7eb7b-c53a-4e7c-888b-dca7802f59eb', restaurant.address), 120)
            }
        )
    return serialized_restaurants
