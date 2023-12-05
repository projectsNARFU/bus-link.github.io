import psycopg2
from peewee import *
from init_db import *


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

def delete_trip(trip_id:int):
    if not BusTrip.get_or_none(BusTrip.id_trip==trip_id):
        print(f'id:{trip_id} среди маршрутов нет в бд')
        return False
    
    deleted_object = BusTrip.delete().where(BusTrip.id_trip==trip_id)
    deleted_object.execute()

if __name__ == '__main__':
    # test_time = ['8:30', '8:40', '8:50', '9:05']
    # add_trip(1, test_time, 1, 1)
    # __update_busstop_trip(trip_id=1, stop_id=2, act_time='8:45', real_time='8:45')
    # update_trip(trip_id=1, list_stop_id=[1, 2, 3, 4], 
    #                     list_act_time=['9:00', '9:15', '9:25', '9:35'],
    #                     driver_id=2, bus_id=2)
    # delete_trip(1)
    pass