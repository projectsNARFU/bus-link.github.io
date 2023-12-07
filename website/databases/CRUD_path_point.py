import psycopg2
from peewee import *
from .init_db import *

def add_path_point(longitude:float, latitude:float):
    if PathPoint.select().where((PathPoint.coord_longitude==longitude) & 
                                     (PathPoint.coord_latitude==latitude)):
        return
    PathPoint.create(coord_longitude=longitude, coord_latitude=latitude)

def update_path_point(id_path_point:int, longitude:float, latitude:float):
    choosed_object = PathPoint.select().where(PathPoint.id_path_point==id_path_point)
    if choosed_object:
        choosed_object = choosed_object.dicts().execute()[0]

        updated_object = PathPoint.update(
            {PathPoint.coord_longitude:longitude, 
             PathPoint.coord_latitude:latitude}).where(
                PathPoint.id_path_point==id_path_point)
        
        updated_object.execute()

def delete_path_point(id_path_point:int):
    deleted_object = PathPoint.delete().where(PathPoint.id_path_point == id_path_point)
    deleted_object.execute()

def get_path_points():
    test = PathPoint.select()
    line_points = []
    for point in test:
        line_points.append([float(point.coord_longitude), float(point.coord_latitude)])
    return line_points

if __name__ == '__main__':
    add_path_point(125.62, 123.94)
    # update_path_point(1, 123.5, 123.8)
    # delete_path_point(1)
    pass