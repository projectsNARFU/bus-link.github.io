import psycopg2
from peewee import *
# from init_db import * -- если вызывать отсюда
from .init_db import *


def add_bus_stop(longitude:float, latitude:float):
    """
    добавляем сущность автобусная остановка
    """
    # сделать условие на проверку вводимых данных
    longitude_exist = BusStop.get_or_none(BusStop.coord_longitude==longitude)
    latitude_exist = BusStop.get_or_none(BusStop.coord_latitude==latitude)
    if not longitude_exist and not latitude_exist:
        busstop, created = BusStop.get_or_create(coord_longitude=longitude, coord_latitude=latitude)

def update_bus_stop_all(values:dict):
    for coords, count_people in values.items():
        # print(coords, count_people)
        updating_values = {'coord_longitude':coords[0],
                           'coord_latitude':coords[1],
                           'number_people':count_people}
        # print(updating_values)
        update_bus_stop(updating_values)

def update_bus_stop(values:dict):
    """
    """
    choosed_object = BusStop.select().where((BusStop.coord_longitude==values['coord_longitude']) &
                                            (BusStop.coord_latitude==values['coord_latitude']))
    # choosed_object = BusStop.select().where(BusStop.id_bus_stop==entered_id)
    if choosed_object:

        choosed_object = choosed_object.dicts().execute()[0]
        # name = values.get('bus_stop_name', choosed_object['bus_stop_name'])
        number_people = values.get('number_people', choosed_object['number_people'])
        # longitude = values.get('coord_longitude', choosed_object['coord_longitude'])
        # latitude = values.get('coord_latitude', choosed_object['coord_latitude'])
        longitude = choosed_object['coord_longitude']
        latitude = choosed_object['coord_latitude']

        # updated_object = BusStop.update(
        #     {BusStop.bus_stop_name:name,
        #      BusStop.number_people:number_people,
        #      BusStop.coord_longitude:longitude, 
        #      BusStop.coord_latitude:latitude}).where(
        #         BusStop.id_bus_stop==entered_id)

        updated_object = BusStop.update(
            {BusStop.number_people:number_people}).where(
                (BusStop.coord_longitude==longitude) &
                (BusStop.coord_latitude==latitude))
        
        updated_object.execute()
    else:
        pass

def delete_bus_stop(stop_id:int):
    """
    """
    # сделать условие на проверку вводимых данных
    choosed_object = BusStop.get_or_none(BusStop.id_bus_stop==stop_id)
    if not choosed_object:
        print('автобуса с таким id нет в бд')
        return
    if choosed_object.routes[:]:

        used_routes = []
        for route in choosed_object.routes:
            used_routes.append(route.id_route)
        used_trips = []
        for route in choosed_object.bus_trips:
            used_trips.append(route.id_route)
        used_routes = sorted(list(set(used_routes)))
        used_trips = sorted(list(set(used_trips)))

        print('эту остановку нельзя удалить из бд,'
                f' т.к. он есть в маршрутах: {used_routes}'
                f' и в рейсах: {used_trips}')
        return
    
    deleted_object = BusStop.delete().where(BusStop.id_bus_stop == stop_id)
    deleted_object.execute()

def get_bus_stop_all():
    bus_stops = BusStop.select()

    coords = []
    count_people = []
    for bus_stop in bus_stops:
        coords.append((bus_stop.coord_longitude, bus_stop.coord_latitude)) 
        count_people.append(bus_stop.number_people)
    dict_variable = dict(zip(coords, count_people))
    return dict_variable

if __name__ == '__main__':
    # add_bus_stop('ostanovka1', 100, 200)
    # test_bus_stop = {'number_people': 4, 'coord_longitude':100, 'coord_latitude':200}
    # update_bus_stop(test_bus_stop)
    # delete_bus_stop(9)
    # update_bus_stop_all({(100, 200): 12, (150.86, 159.9): 1})
    stops = [(64.54161, 40.39945), (64.53747, 40.41655), 
             (64.53537, 40.43097), (64.53382, 40.44243), 
             (64.53206, 40.45398), (64.53209, 40.46036), 
             (64.53297, 40.4708)]
    # for stop in stops:
    #      add_bus_stop(stop[0], stop[1])
    # update_bus_stop_all()
    print(get_bus_stop_all())
    pass