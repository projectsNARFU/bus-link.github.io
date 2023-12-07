import psycopg2
from peewee import *
from .init_db import *
from .CRUD_path_point import *

def add_route_path(route_id:int, input_list_coords:str):
    raw_list_coords = input_list_coords.replace('[', '')
    raw_list_coords = raw_list_coords.replace(']', '')
    raw_list_coords = raw_list_coords.replace(' ', '')
    raw_list_coords = raw_list_coords.split(',')
    list_coords = []
    for i in range(0, len(raw_list_coords)-1, 2):
        list_coords.append([raw_list_coords[i], raw_list_coords[i+1]])
    
    for coords in list_coords:
        add_path_point(coords[0], coords[1])
        new_path_point = PathPoint.select().where((PathPoint.coord_longitude==coords[0]) &
                                                  (PathPoint.coord_latitude==coords[1]))
        # print(PathPoint.select()[:])
        add_route_path_point(route_id, new_path_point[0].id_path_point)

def add_route_path_point(route_id:int, path_point_id:int):
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
    # add_route_path_point(1, 5)
    # update_route_path(1, 6)
    # delete_route_path(1)
    # raw_list = str([[12.12,13.56],[1.34,12.99]])
    # add_route_path(route_id=1, input_list_coords=raw_list)
    pass