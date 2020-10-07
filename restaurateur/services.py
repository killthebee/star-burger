def find_restaurant(restaurants_and_items, order_items):

    possible_restaurants = []
    for order_item in order_items:
        for restaurant_and_items in restaurants_and_items:
            if order_item in restaurant_and_items[1]:
                possible_restaurants.append(restaurant_and_items[0])
    return set(possible_restaurants)
