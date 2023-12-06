import psycopg2
from peewee import *

db = PostgresqlDatabase('postgres', host='localhost', port=5432, 
                        user='postgres', password='qwer')


class BaseModel(Model):
    class Meta:
        database = db  


class BusStop(BaseModel):
    id_bus_stop = AutoField()
    number_people = IntegerField(null=False , default=0)
    bus_stop_name = TextField(null=False, unique=True)
    coord_longitude = FloatField(default=0)
    coord_latitude = FloatField(default=0)
    class Meta:
        table_name = 'bus_stop'


class Bus(BaseModel):
    id_bus = AutoField()
    bus_number = IntegerField(null=False)
    charge_level = IntegerField(null=False, default=0)
    number_passenger = IntegerField(null=False, default=0)
    class Meta:
        table_name = 'bus'


class Driver(BaseModel):
    id_driver = AutoField()
    full_name = TextField(null=False)
    email = TextField(null=False, unique=True)
    password = TextField(null=False)
    nonstop = IntegerField(null=False, default=0)
    class Meta:
        table_name = 'driver'


class Route(BaseModel):
    """
    благодаря backref можно будет через остановку, 
    вывести все маршруты, в кот. есть эта остановка
    """
    id_route = IntegerField(null=False)
    id_bus_stop = ForeignKeyField(BusStop, backref='routes')
    serial_num_bustop = IntegerField(null=False)
    distance_previous_busstop = FloatField(default=0)
    class Meta:
        table_name = 'route'
        primary_key = CompositeKey('id_route', 'id_bus_stop')


class BusTrip(BaseModel):
    """
    в peewee составной внешний ключ не завезли, 
    поэтому маршрут и рейс связать не могу
    """
    id_trip = IntegerField(null=False)
    id_route = IntegerField(null=False)
    id_bus_stop = ForeignKeyField(BusStop, backref='bus_trips')
    actual_arrival_time = TimeField(null=False)
    real_arrival_time = TimeField(null=False)
    id_driver = ForeignKeyField(Driver, backref='bus_trips')
    id_bus = ForeignKeyField(Bus, backref='bus_trips')
    class Meta:
        table_name = 'bus_trip'
        primary_key = CompositeKey('id_trip', 'id_bus_stop')

    
class RoutePath(BaseModel):
    """"""
    id_route_path = AutoField()
    coord_longitude = FloatField(default=0)
    coord_latitude = FloatField(default=0)
    class Meta:
        table_name = 'route_path'


def init_dbs():
    """db.execute_sql() поможет ли?"""
    cur = db.cursor()

    db.create_tables([BusStop, Bus, Driver, Route])

    cur.execute('DROP TABLE IF EXISTS bus_trip;')
    cur.execute("""CREATE TABLE bus_trip (
                id_trip integer NOT NULL,
                id_route integer NOT NULL,
                id_bus_stop integer NOT NULL,
                actual_arrival_time time NOT NULL,
                real_arrival_time time NOT NULL,
                id_driver integer NOT NULL,
                id_bus integer NOT NULL,
                PRIMARY KEY (id_trip, id_bus_stop),
                FOREIGN KEY (id_route, id_bus_stop) REFERENCES route (id_route, id_bus_stop),
                FOREIGN KEY (id_bus_stop) REFERENCES bus_stop (id_bus_stop),
                FOREIGN KEY (id_driver) REFERENCES driver (id_driver),
                FOREIGN KEY (id_bus) REFERENCES bus (id_bus)
                );
                """)
    db.commit()
    
    cur.close()
    db.close()


if __name__ == '__main__':
    # init_dbs()
    db.create_tables([BusStop, Bus, Driver, Route, BusTrip, RoutePath])
