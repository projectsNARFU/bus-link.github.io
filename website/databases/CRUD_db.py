import psycopg2
from peewee import *
from init_db import *

"""
здесь находятся функции взаимодействия с бд
и рекомендации того, как и что с ними делать
"""

def add_bus_stop(name:str, coord:str):
    """
    добавляем сущность автобусная остановка
    """
    # сделать условие на проверку вводимых данных
    name_exist = BusStop.get_or_none(BusStop.bus_stop_name==name)
    coord_exist = BusStop.get_or_none(BusStop.coords==coord)
    if not name_exist and not coord_exist:
        busstop, created = BusStop.get_or_create(bus_stop_name=name, coords=coord)

def update_bus_stop(values:dict):
    """
    """
    # сделать условие на проверку вводимых данных
    entered_id = values['id_bus_stop']
    choosed_object = BusStop.select().where(BusStop.id_bus_stop==entered_id)
    if choosed_object:

        choosed_object = choosed_object.dicts().execute()[0]
        name = values.get('bus_stop_name', choosed_object['bus_stop_name'])
        coord = values.get('coords', choosed_object['coords'])

        updated_stop = BusStop.update(
            {BusStop.bus_stop_name:name, BusStop.coords:coord}).where(
                BusStop.id_bus_stop==entered_id)
        
        updated_stop.execute()
    else:
        pass

def delete_bus_stop(stop_id:int):
    """
    """
    # сделать условие на проверку вводимых данных
    choosed_stop = BusStop.get_or_none(BusStop.id_bus_stop==stop_id)
    if choosed_stop:
        if choosed_stop.routes[:]:

            used_routes = []
            for route in choosed_stop.routes:
                used_routes.append(route.id_route)
            used_trips = []
            for route in choosed_stop.bus_trips:
                used_trips.append(route.id_route)
            used_routes = sorted(list(set(used_routes)))
            used_trips = sorted(list(set(used_trips)))

            print('эту остановку нельзя удалить из бд,'
                    f' т.к. он есть в маршрутах: {used_routes}'
                    f' и в рейсах: {used_trips}')
        else:
            deleted_object = BusStop.delete().where(BusStop.id_bus_stop == stop_id)
            deleted_object.execute()
    else:
        print('автобуса с таким id нет в бд')

def add_bus(bus_num:int):
    """
    добавляем сущность автобус
    """
    # сделать условие на проверку вводимых данных
    Bus.create(bus_number=bus_num)

def update_bus(values:dict):
    """
    """
    # сделать условие на проверку вводимых данных
    entered_id = values['id_bus']
    choosed_object = Bus.select().where(Bus.id_bus==entered_id)
    if choosed_object:
        choosed_object = choosed_object.dicts().execute()[0]

        bus_num = values.get('bus_number', choosed_object['bus_number'])

        updated_object = Bus.update(
            {Bus.bus_number:bus_num}).where(
                Bus.id_bus==entered_id)
        
        updated_object.execute()

def delete_bus(bus_id:int):
    """
    """
    # сделать условие на проверку вводимых данных
    choosed_object = Bus.get_or_none(Bus.id_bus==bus_id)
    if choosed_object:
        if choosed_object.bus_trips[:]:

            # used_routes = []
            # for route in choosed_stop.routes:
            #     used_routes.append(route.id_route)
            used_trips = []
            for route in choosed_object.bus_trips:
                used_trips.append(route.id_route)
            used_trips = sorted(list(set(used_trips)))

            print('этот автобус нельзя удалить из бд,'
                    f' т.к. он есть в рейсах: {used_trips}')
        else:
            deleted_object = Bus.delete().where(Bus.id_bus == bus_id)
            deleted_object.execute()
    else:
        print('автобуса с таким id нет в бд')

def add_driver(full_name:str, email:str, password:str):
    """
    добавляем сущность автобусная остановка
    """
    # сделать условие на проверку вводимых данных
    email_exist = Driver.get_or_none(Driver.email==email)
    if not email_exist:
        driver, created = Driver.get_or_create(full_name=full_name, email=email, password=password)

def update_driver(values:dict):
    """
    """
    # сделать условие на проверку вводимых данных
    entered_id = values['id_driver']
    choosed_object = Driver.select().where(Driver.id_driver==entered_id)
    if choosed_object:

        choosed_object = choosed_object.dicts().execute()[0]
        full_name = values.get('full_name', choosed_object['full_name'])
        email = values.get('email', choosed_object['email'])
        password = values.get('password', choosed_object['password'])

        updated_object = Driver.update(
            {Driver.full_name:full_name, Driver.email:email, Driver.password:password}).where(
                Driver.id_driver==entered_id)
        
        updated_object.execute()
    else:
        pass

def delete_driver(driver_id:int):
    """
    """
    # сделать условие на проверку вводимых данных
    choosed_object = Driver.get_or_none(Driver.id_driver==driver_id)
    if choosed_object:
        if choosed_object.bus_trips[:]:

            used_trips = []
            for trip in choosed_object.bus_trips:
                used_trips.append(trip.id_trip)
            used_trips = sorted(list(set(used_trips)))

            print('этого водителя нельзя удалить из бд,'
                    f' т.к. он есть в рейсах: {used_trips}')
        else:
            deleted_object = Driver.delete().where(Driver.id_driver == driver_id)
            deleted_object.execute()
    else:
        print('автобуса с таким id нет в бд')

if __name__ == '__main__':
    add_bus_stop(61, '125.64')
    test_bus_stop = {'id_bus_stop': 17, 'coords': '228.228'}
    update_bus_stop(test_bus_stop)
    # delete_bus_stop(9)
    # add_bus(1)
    test_bus = {'id_bus': 2, 'bus_number': 76}
    update_bus(test_bus)
    # delete_bus(3)
    add_driver('zubenko mikhail petrovich', 'mafioznik@mail.ru', 'gangstaVlast')
    test_driver = {'id_driver': 1, 'password': 'fhdusSD12'}
    update_driver(test_driver)
    delete_driver(1)