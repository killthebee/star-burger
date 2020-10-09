import os
import requests
from geopy import distance
from dotenv import load_dotenv
load_dotenv()


def fetch_coordinates(apikey, place):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    params = {"geocode": place, "apikey": apikey, "format": "json"}
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    places_found = response.json()['response']['GeoObjectCollection']['featureMember']
    most_relevant = places_found[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lon, lat


def add_distanсes(restaurants, order_coords):
    for restaurant in restaurants:
        restaurant['delivery_distance'] = round(distance.distance(restaurant['coords'], order_coords).km, 2)
    return restaurants


def find_restaurants(restaurants_and_items, order):
    order_coords = fetch_coordinates('5dc7eb7b-c53a-4e7c-888b-dca7802f59eb', order.address)
    order_items = [product.product.name for product in order.order_products.all()]
    possible_restaurants = []
    for order_item in order_items:
        for restaurant_and_items in restaurants_and_items:
            if order_item in restaurant_and_items[1]:
                possible_restaurant_address = restaurant_and_items[0].address
                restaurant_coords = fetch_coordinates('5dc7eb7b-c53a-4e7c-888b-dca7802f59eb', possible_restaurant_address)
                possible_restaurant = {
                    'name': restaurant_and_items[0].name,
                    'coords': restaurant_coords
                }
                possible_restaurants.append(possible_restaurant)

    uniq_possible_restaurants = list({v['name']:v for v in possible_restaurants}.values())
    possible_restaurants = add_distanсes(uniq_possible_restaurants, order_coords)
    return possible_restaurants



