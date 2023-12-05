import psycopg2
from peewee import *
from init_db import *


def add_driver(full_name:str, email:str, password:str):
    """
    добавляем сущность автобусная остановка
    """
    # сделать условие на проверку вводимых данных
    email_exist = Driver.get_or_none(Driver.email==email)
    if not email_exist:
        driver, created = Driver.get_or_create(full_name=full_name, email=email, password=password)
    else:
        print('email занят')

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
    if not choosed_object:
        print(f'автобуса с id:{driver_id} нет в бд')
        return

    if choosed_object.bus_trips[:]:

        used_trips = []
        for trip in choosed_object.bus_trips:
            used_trips.append(trip.id_trip)
        used_trips = sorted(list(set(used_trips)))

        print('этого водителя нельзя удалить из бд,'
                f' т.к. он есть в рейсах: {used_trips}')
        return
    
    deleted_object = Driver.delete().where(Driver.id_driver == driver_id)
    deleted_object.execute()

if __name__ == '__main__':
    # add_driver('ivanov ivan ivanovich', 'ivanov1980@mail.ru', 'qwerty123')
    # test_driver = {'id_driver': 1, 'password': 'fhdusSD12'}
    # update_driver(test_driver)
    # delete_driver(1234)
    pass
