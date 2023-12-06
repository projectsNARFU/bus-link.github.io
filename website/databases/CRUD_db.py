import psycopg2
from peewee import *
from init_db import *

"""
здесь находятся функции взаимодействия с бд
и рекомендации того, как и что с ними делать
"""

def calc_distance(prev_stop, cur_stop):
    """вместо этой функции, будет расчет расстояния между остановками"""
    return 0.5

# BUS STOP

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

        updated_object = BusStop.update(
            {BusStop.bus_stop_name:name, BusStop.coords:coord}).where(
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

# BUS

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

# DRIVER

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

# ROUTE

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

# BUS TRIP

def add_trip(route_id:int, arrival_time:list, driver_id:int, bus_id:int):
    """"""
    return __add_trip(route_id, arrival_time, driver_id, bus_id)

def __add_trip(route_id:int, arrival_time:list, driver_id:int, bus_id:int, default_trip_id:int=-1):
    """"""

    if not Route.get_or_none(Route.id_route==route_id):
        print(f'id:{route_id} среди маршрутов нет в бд')
        return False
    if not Driver.get_or_none(Driver.id_driver==driver_id):
        print(f'id:{driver_id} среди водителей нет в бд')
        return False
    if not Bus.get_or_none(Bus.id_bus==bus_id):
        print(f'id:{bus_id} среди автобусов нет в бд')
        return False
    
    choosed_object = Route.select().where(Route.id_route==route_id)
    if len(choosed_object[:]) != len(arrival_time):
        print(f'количество расписаний ({len(arrival_time)}) не совпадает с '
            f'количеством остановок в маршруте {route_id} ({len(choosed_object[:])})')
        return False
    
    #  СДЕЛАТЬ ПРОВЕРКУ ЧТО В СПИСКЕ ИМЕННО ВРЕМЯ, А НЕ ЧТО-ТО ДРУГОЕ

    cur_max = BusTrip.select(fn.MAX(BusTrip.id_trip)).scalar()
    if not cur_max:
        new_id = max(default_trip_id, 1)
    elif default_trip_id == -1:
        new_id = cur_max + 1
    else:
        new_id = default_trip_id
    
    cur_add_time = 0
    for busstop_route in choosed_object[:]:
        BusTrip.create(id_trip=new_id, id_route=route_id, id_bus_stop=busstop_route.id_bus_stop,
                        actual_arrival_time=arrival_time[cur_add_time], 
                        real_arrival_time=arrival_time[cur_add_time], id_driver=driver_id, id_bus=bus_id)
        cur_add_time += 1

def update_trip(trip_id:int, list_stop_id:list=[], list_act_time:list=[], driver_id:int=-1, bus_id:int=-1):
    """
    обновление расписания рейса, изменение автобуса и водителя
    назначенных на рейс. Вызывается из фронта.
    """
    if not BusTrip.get_or_none(BusTrip.id_trip==trip_id):
        print(f'id:{trip_id} среди рейсов нет в бд')
        return False
    # print(len(BusTrip.select().where(BusTrip.id_trip == trip_id)[:]))
    trip = BusTrip.select().where(BusTrip.id_trip == trip_id)
    for par in [list_stop_id, list_act_time]:
        if len(par) > len(trip[:]):
            print(f'в списке {par} введено больше значений, чем находится в маршруте')
            return False
    if (driver_id!=-1) and (not Driver.get_or_none(Driver.id_driver==driver_id)):
        print(f'id:{driver_id} среди водителей нет в бд')
        return False
    if (bus_id!=-1) and (not Bus.get_or_none(Bus.id_bus==bus_id)):
        print(f'id:{bus_id} среди автобусов нет в бд')
        return False
    
    if driver_id != -1:
        driver_id = driver_id
    else:
        driver_id = trip[0].id_driver
    if bus_id != -1:
        bus_id = bus_id
    else:
        bus_id = trip[0].id_bus
    for i in range(len(list_stop_id)):
        __update_busstop_trip(trip_id=trip_id, stop_id=list_stop_id[i],
                                 act_time=list_act_time[i], real_time=list_act_time[i],
                                 driver_id=driver_id, bus_id=bus_id)

def __update_busstop_trip(trip_id:int, stop_id:int, act_time:str=None, real_time:str=None, driver_id:int=-1, bus_id:int=-1):
    """
    Обновление информации по одной остановке в маршруте.
    это внутренняя функция, расчитанная на изменение актуального времени
    и реального времени (то есть подразумевается, что это функция используется
    только в бекенде). Через эту функцию мы фиксируем несостыковку с
    назначенным и реальным временем
    """
    choosed_route = BusTrip.select().where((BusTrip.id_trip==trip_id) & (BusTrip.id_bus_stop==stop_id))
    if not choosed_route:
        print(f'в выбраном рейсе {trip_id}, нет остановки {stop_id}')
        return False
    if (driver_id!=-1) and (not Driver.get_or_none(Driver.id_driver==driver_id)):
        print(f'id:{driver_id} среди водителей нет в бд')
        return False
    if (bus_id!=-1) and (not Bus.get_or_none(Bus.id_bus==bus_id)):
        print(f'id:{bus_id} среди автобусов нет в бд')
        return False
    
    

    # ПРОВЕРКИ ТОГО, ЧТО РАСПИСАНИЯ ВВЕДЕНЫ КОРРЕКТНО
    
    if act_time:
        act_time = act_time
    else:
        act_time = choosed_route[0].actual_arrival_time
    if real_time:
        real_time = real_time
    else:
        real_time = choosed_route[0].real_arrival_time
    if driver_id != -1:
        driver_id = driver_id
    else:
        driver_id = choosed_route[0].id_driver
    if bus_id != -1:
        bus_id = bus_id
    else:
        bus_id = choosed_route[0].id_bus

    changed_object = BusTrip.update({BusTrip.actual_arrival_time:act_time, 
                                     BusTrip.real_arrival_time:real_time,
                                     BusTrip.id_driver:driver_id,
                                     BusTrip.id_bus:bus_id}).where(
            (BusTrip.id_trip==trip_id) & (BusTrip.id_bus_stop==stop_id))
    changed_object.execute()
    return True

if __name__ == '__main__':
    # add_bus_stop('stoyanka', '150.64')
    # test_bus_stop = {'id_bus_stop': 17, 'coords': '228.228'}
    # update_bus_stop(test_bus_stop)
    # delete_bus_stop(9)
    # add_bus(9)
    # test_bus = {'id_bus': 2, 'bus_number': 76}
    # update_bus(test_bus)
    # delete_bus(3)
    # add_driver('ivanov ivan ivanovich', 'ivanov1980@mail.ru', 'qwerty123')
    # test_driver = {'id_driver': 1, 'password': 'fhdusSD12'}
    # update_driver(test_driver)
    # delete_driver(1234)
    # add_route([1, 2, 3, 4])
    # update_busstop_route(2, 7, 1)
    # update_busstop_route(1, 7, 2)
    # delete_route(1)
    # delete_busstop_route(2, 7)
    # test_time = ['8:30', '8:40', '8:50', '9:05']
    # add_trip(1, test_time, 1, 1)
    # __update_busstop_trip(trip_id=1, stop_id=2, act_time='8:45', real_time='8:45')
    # update_trip(trip_id=1, list_stop_id=[1, 2, 3, 4], 
    #                     list_act_time=['9:00', '9:15', '9:25', '9:35'],
    #                     driver_id=2, bus_id=2)
    pass
