import psycopg2
from peewee import *
from init_db import *

def add_route_path(route_id:int, path_point_id:int):
    RoutePath.create(id_route=route_id, id_path_point=path_point_id)

def update_route_path(id_route_path:int, path_point_id:int):
    choosed_object = RoutePath.select().where(RoutePath.id_route_path==id_route_path)
    if choosed_object:
        choosed_object = choosed_object.dicts().execute()[0]

        updated_object = RoutePath.update(
            {RoutePath.id_path_point:path_point_id}).where(
                RoutePath.id_route_path==id_route_path)
        
        updated_object.execute()

def delete_route_path_point(id_route_path:int, path_point_id:int):
    """удаляем точку в пути маршрута"""
    deleted_object = RoutePath.delete().where(RoutePath.id_route_path == id_route_path)
    deleted_object.execute()

def delete_route_path(route_id:int):
    """удаляем весь путь маршрута"""
    deleted_object = RoutePath.delete().where(RoutePath.id_route == route_id)
    deleted_object.execute()

if __name__ == '__main__':
    # add_route_path(1, 5)
    # update_route_path(1, 6)
    delete_route_path(1)
    pass