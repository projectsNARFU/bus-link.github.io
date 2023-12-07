import psycopg2
from peewee import *
from init_db import *


def calc_distance(prev_stop, cur_stop):
    """вместо этой функции, будет расчет расстояния между остановками"""
    return 0.5

def add_route(bus_stop_list:list):
    """
    добавляем сущность автобусная остановка
    """
    return __add_route(bus_stop_list)

def __add_route(bus_stop_list:list, default_route_id:int=-1):
    """
    добавляем сущность автобусная остановка
    """

    # проверка маршрут будет составлен как минимум из 2 остановок
    if len(bus_stop_list)<2:
        print('маршрут должен состоять хотя бы из 2 остановок!')
        return False
    
    if default_route_id == 0:
        print('id маршрута не может быть равен 0')
        return False

    # проверка на повторки
    if len(bus_stop_list) != len(set(bus_stop_list)):
        print('остановки не должны повторяться!')
        return 

    # провера, что введенные id остановки есть в бд
    # еще проверка, что введенные id остановки являются числами
    not_existed_stops = []
    for stop_id in bus_stop_list:
        if not str(stop_id).isdigit():
            print('должны быть введены только числа!')
            return
        if not BusStop.get_or_none(BusStop.id_bus_stop==stop_id):
            not_existed_stops.append(stop_id)
    if not_existed_stops:
        print(f'этих остановок не существует в бд: {not_existed_stops}')
        return False
    
    # не проверял, но вроде ок
    cur_max = Route.select(fn.MAX(Route.id_route)).scalar()
    if not cur_max:
        new_id = max(default_route_id, 1)
    elif default_route_id == -1:
        new_id = cur_max + 1
    else:
        new_id = default_route_id

    # прошлый вариант
    # cur_max = Route.select(fn.MAX(Route.id_route)).scalar()
    # new_id = max(default_route_id, cur_max)
    # if not new_id:
    #     new_id = max(1, default_route_id)
    # elif cur_max and default_route_id > cur_max:
    #     new_id = new_id
    # else: 
    #     new_id += 1
    
    for i in range(len(bus_stop_list)):
        if i == 0:
            distance = 0
        else:
            distance = calc_distance(bus_stop_list[i-1], bus_stop_list[i])
        Route.create(id_route=new_id, id_bus_stop=bus_stop_list[i],
                        serial_num_bustop=i+1, distance_previous_busstop=distance)
    return True

def update_busstop_route(route_id:int, stop_id:int, serial_num:int):
    choosed_object = BusStop.get_or_none(BusStop.id_bus_stop==stop_id)

    # ПРОВЕРКА, ЕСТЬ ЛИ ВВЕДЕННАЯ ОСТАНОВКА В ДБ
    # ПРОВЕРКА, НОРМАЛЬНЫЙ ЛИ ПОРЯДКОВЫЙ НОМЕР (НЕ НАМНОГО ОН БОЛЬШЕ МАКС ЗНАЧЕНИЯ?)

    routes = []
    for route in choosed_object.routes[:]:
        routes.append(route.id_route)
    
    if not (route_id in routes):
        print('этой остановки нет в маршруте')
        some_route = Route.select().where(Route.id_route==route_id).order_by(Route.serial_num_bustop)
        for bus_stop_route in some_route:
            if bus_stop_route.serial_num_bustop >= serial_num:
                bus_stop_route.serial_num_bustop += 1
                bus_stop_route.save()
        Route.create(id_route=route_id, id_bus_stop=stop_id,
                        serial_num_bustop=serial_num, distance_previous_busstop=0)
        return True
    else:
        print('эта остановка уже есть в маршруте!')
        some_route = Route.select().where(Route.id_route==route_id).order_by(Route.serial_num_bustop)
        for bus_stop_route in some_route:
            
            old_ser_num = some_route.where(Route.id_bus_stop==stop_id)[0].serial_num_bustop

            # если новое значение больше старого
            if old_ser_num < bus_stop_route.serial_num_bustop <= serial_num:
                bus_stop_route.serial_num_bustop -= 1
                bus_stop_route.save()
            # если новое значение меньше старого
            elif serial_num <= bus_stop_route.serial_num_bustop < old_ser_num:
                bus_stop_route.serial_num_bustop += 1
                bus_stop_route.save()
        changed_object = Route.update({Route.serial_num_bustop:serial_num}).where(
            (Route.id_route==route_id) & (Route.id_bus_stop==stop_id))
        changed_object.execute()
        return True

def update_busstop_route_cascade(route_id:int, stop_id:int, serial_num:int):
    pass

def delete_route(route_id:int):
    choosed_object = Route.select().where(Route.id_route==route_id)
    if not choosed_object:
        print(f'маршрута с id:{route_id} нет в бд')
        return False
    
    trips = choosed_object[0].id_bus_stop.bus_trips[:]
    used_trips = []
    for trip in trips:
        if trips[0].id_route == route_id:
            used_trips.append(trip.id_trip)
    used_trips = sorted(list(set(used_trips)))

    if used_trips:
        print('этот маршрут нельзя удалить из бд,'
                f' т.к. он есть в рейсах: {used_trips}')
        return False
    
    deleted_object = Route.delete().where(Route.id_route==route_id)
    deleted_object.execute()
    return True

def delete_route_cascade(route_id:int):
    """удаляет маршрут и все рейсы этого маршрута"""
    pass

def delete_busstop_route(route_id:int, stop_id:int):
    choosed_object = Route.select().where(Route.id_route==route_id)
    contained_bus_stops = []
    for busstop in choosed_object[:]:
        if busstop.id_bus_stop.id_bus_stop != stop_id:
            contained_bus_stops.append(busstop.id_bus_stop.id_bus_stop)
    if delete_route(route_id):
        return __add_route(contained_bus_stops, route_id-1)
    else:
        return False

def delete_busstop_route_cascade(route_id:int, stop_id:int):
    pass

if __name__ == '__main__':
    add_route([1, 2, 3, 4])
    # update_busstop_route(2, 7, 1)
    # update_busstop_route(1, 7, 2)
    # delete_route(1)
    # delete_busstop_route(2, 7)
    pass