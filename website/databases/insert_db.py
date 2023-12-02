import psycopg2
from peewee import *
from init_db import *

"""
добавление записей (чисто руками пока что)
"""
# BusStop.create(number_people=7, bus_stop_name='vorona',
#                 coords='123.21.1')
# BusStop.create(number_people=10, bus_stop_name='volk',
#                 coords='100.8.8')
# BusStop.create(number_people=1, bus_stop_name='zayats',
#                 coords='112.75.82')
# BusStop.create(number_people=7, bus_stop_name='sobaka',
#                 coords='150.2.1')
# BusStop.create(number_people=5, bus_stop_name='koshka',
#                 coords='170.44.1')
# Driver.create(full_name='ivanov ivan ivanovich', email='ivanovich1980@mail.ru',
#                 password='qwerty')
# Bus.create(bus_number=42)

# Route.create(id_route=1, id_bus_stop=3, serial_num_bustop=1, distance_previous_busstop=0)
# Route.create(id_route=1, id_bus_stop=1, serial_num_bustop=2, distance_previous_busstop=0.8)
# Route.create(id_route=1, id_bus_stop=2, serial_num_bustop=3, distance_previous_busstop=0.5)
# Route.create(id_route=1, id_bus_stop=4, serial_num_bustop=4, distance_previous_busstop=0.5)

# BusTrip.create(id_trip=1, id_route=1, id_bus_stop=3, actual_arrival_time='8:00',
#                 real_arrival_time='8:00', id_driver=1, id_bus=1)
# BusTrip.create(id_trip=1, id_route=1, id_bus_stop=1, actual_arrival_time='8:10',
#                 real_arrival_time='8:10', id_driver=1, id_bus=1)
# BusTrip.create(id_trip=1, id_route=1, id_bus_stop=2, actual_arrival_time='8:20',
#                 real_arrival_time='8:20', id_driver=1, id_bus=1)
# BusTrip.create(id_trip=1, id_route=1, id_bus_stop=4, actual_arrival_time='8:30',
#                 real_arrival_time='8:30', id_driver=1, id_bus=1)

"""
изменение записей
"""
# some_busstop = BusStop(number_people='0')
# some_busstop.id_bus_stop = 1  
# some_busstop.save()

# some_route=Route.get((Route.id_route==1) & (Route.id_bus_stop==3))
# some_route = Route(id_route=1, id_bus_stop=3)
# print(some_route)
# some_route.id_bus_stop = 6
# # some_route = Route(id_bus_stop=6)
# # some_route.route_pkey = (1, 3)
# some_route.save()

# some_route=Route.update({Route.id_bus_stop:6}).where(
#     (Route.id_bus_stop==3) & (Route.id_route==1)
#     )
# print (some_route.sql())
# some_route.execute()

# some_trip=BusTrip.update({BusTrip.actual_arrival_time:'8:40'}).where(
#     (BusTrip.id_trip==1) & (BusTrip.id_bus_stop==4)
#     )
# some_trip.execute()

"""
удаление записей
"""
# deleted_bus_stop = BusStop.delete().where(BusStop.id_bus_stop == 6)
# deleted_bus_stop.execute()

"""вызовет ошибку, т.к. автобус подвязан к рейсу
нужно, чтобы в такой ситуации, он просто вывел текст
'вы не можете удалить автобус из бд, т.к. 
он подвязан к рейсу/ам {вставьте список рейсов}'"""
# deleted_bus = Bus.delete().where(Bus.id_bus == 1)
# deleted_bus.execute()

"""с водителем та же тема"""

"""если мы удаляем часть или весь маршрут, это должно измениться для всех рейсов
этого маршрута"""
# delete_route = Route.delete().where((Route.id_bus_stop_id==1) & (Route.id_route==1))
# delete_route.execute()

"""по-логике, мы не можем удалить остановку в рейсе, либо удаляем в маршруте остановку, либо 
удаляем рейс полностью"""
# delete_trip = BusTrip.delete().where((BusTrip.id_bus_stop_id==1) & (BusTrip.id_trip==1))
# delete_trip.execute()

"""
просмотр записей
"""

"""можно легко вывести один или несколько строк
в качестве словаря/-ей"""
# a_bus = Bus.select().where(Bus.id_bus==1)
# bus_selected = a_bus.dicts().execute()
# print(bus_selected[0])

# a_route = Route.select().where(Route.id_route==1)
# route_selected = a_route.dicts().execute()
# for route_stop in route_selected:
#     print(route_stop)