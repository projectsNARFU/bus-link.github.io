import psycopg2
from peewee import *
from init_db import *


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
    if not choosed_object:
        print('автобуса с таким id нет в бд')
        return
    
    if choosed_object.bus_trips[:]:

        used_trips = []
        for route in choosed_object.bus_trips:
            used_trips.append(route.id_trip)
        used_trips = sorted(list(set(used_trips)))

        print('этот автобус нельзя удалить из бд,'
                f' т.к. он есть в рейсах: {used_trips}')
        return
    
    deleted_object = Bus.delete().where(Bus.id_bus == bus_id)
    deleted_object.execute()

if __name__ == '__main__':
    pass
    # add_bus(9)
    # test_bus = {'id_bus': 2, 'bus_number': 76}
    # update_bus(test_bus)
    # delete_bus(3)