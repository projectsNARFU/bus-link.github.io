import psycopg2
from peewee import *
# from init_db import * -- если вызывать отсюда
from .init_db import *


def add_bus_stop(name:str, longitude:float, latitude:float):
    """
    добавляем сущность автобусная остановка
    """
    # сделать условие на проверку вводимых данных
    name_exist = BusStop.get_or_none(BusStop.bus_stop_name==name)
    longitude_exist = BusStop.get_or_none(BusStop.coord_longitude==longitude)
    latitude_exist = BusStop.get_or_none(BusStop.coord_latitude==latitude)
    if not name_exist and not longitude_exist and not latitude_exist:
        busstop, created = BusStop.get_or_create(bus_stop_name=name, coord_longitude=longitude, coord_latitude=latitude)

def update_bus_stop(values:dict):
    """
    """
    # сделать условие на проверку вводимых данных
    entered_id = values['id_bus_stop']
    choosed_object = BusStop.select().where(BusStop.id_bus_stop==entered_id)
    if choosed_object:

        choosed_object = choosed_object.dicts().execute()[0]
        name = values.get('bus_stop_name', choosed_object['bus_stop_name'])
        longitude = values.get('coord_longitude', choosed_object['coord_longitude'])
        latitude = values.get('coord_latitude', choosed_object['coord_latitude'])

        updated_object = BusStop.update(
            {BusStop.bus_stop_name:name, 
             BusStop.coord_longitude:longitude, 
             BusStop.coord_latitude:latitude}).where(
                BusStop.id_bus_stop==entered_id)
        
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

if __name__ == '__main__':
    add_bus_stop('ostanovka', 150.86, 159.9)
    # test_bus_stop = {'id_bus_stop': 17, 'coord_longitude': 222.233, 'coord_latitude': 90.8}
    # update_bus_stop(test_bus_stop)
    # delete_bus_stop(9)
    pass