import random

from geopy.distance import geodesic

# проверка сколько остановок проехал автобус до нажатия кнопки
def bus_on_stop(_stop_coordinates, _current_bus_coord):
    stop_passed = set()
    threshold = 0.1  # Пороговое расстояние (в километрах)
    for stop_coord in _stop_coordinates.keys():
        stop_passed.add(stop_coord)
        distance = geodesic(_current_bus_coord, stop_coord).kilometers
        if distance <= threshold:
            # print(stop_passed, 'SET FROM bus_on_stop')
            return stop_passed
    # нужно исправить
    return []


def passengers_on_stops(stops):
    for i, key in enumerate(stops):
        print(f'i:{i}, key:{key}')
        if i == 0:
            stops[key] = random.randint(0, 20)
        elif i == len(stops) - 1:
            stops[key] = 0
        else:
            stops[key] = random.randint(0, 10)
    # print("изначальная генерация людей на остановках")
    # print(stops)
    return stops


def change_passengers(bus_location, stops):
    # генерируем изначальное количество пассажиров, можно вызывать отдельно от этой функции
    # stops = passengers_on_stops(stops)
    # max_value = 25
    for coords, passengers in stops.items():
        # проверяем был ли автобус на остановках
        # print(coords, stops, bus_location, 'PROBLEM')
        if coords in bus_on_stop(stops, bus_location):
            if passengers >= 10:
                print(bus_location, 'location')
                passengers -= 10
            else:
                passengers = 0
        elif coords == list(stops.keys())[-1]:
            pass
        else:
            passengers += random.randint(0, 5)
            # if  passengers > max_value:
            #     passengers = max_value
        stops[coords] = passengers
    # print("количество людей на остановках при нажатии на кнопку(нужны координаты автобуса в данное время)")
    return stops

# current_location = (64.54150, 40.39990)
# stops_dict = {(64.54161, 40.39945): 0, (64.53747, 40.41655): 0, (64.53537, 40.43097): 0, (64.53382, 40.44243): 0,
#          (64.53206, 40.45398): 0, (64.53209, 40.46036): 0, (64.53297, 40.4708): 0}

# stops = passengers_on_stops(stops_dict)

# print(change_passengers(current_location, stops_dict))

