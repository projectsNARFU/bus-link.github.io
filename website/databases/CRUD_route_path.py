import psycopg2
from peewee import *
from .init_db import *

def add_route_path(longitude:float, latitude:float):
    RoutePath.create(coord_longitude=longitude, coord_latitude=latitude)

def update_route_path(id_route_path:int, longitude:float, latitude:float):
    choosed_object = RoutePath.select().where(RoutePath.id_route_path==id_route_path)
    if choosed_object:
        choosed_object = choosed_object.dicts().execute()[0]

        updated_object = RoutePath.update(
            {RoutePath.coord_longitude:longitude, 
             RoutePath.coord_latitude:latitude}).where(
                RoutePath.id_route_path==id_route_path)
        
        updated_object.execute()

def delete_route_path(id_route_path:int):
    deleted_object = RoutePath.delete().where(RoutePath.id_route_path == id_route_path)
    deleted_object.execute()

if __name__ == '__main__':
    # add_route_path(123.32, 123.654)
    # update_route_path(1, 123.5, 123.8)
    # delete_route_path(1)
    pass