import os
import psycopg2

conn = psycopg2.connect(
        host='localhost',
        dbname='postgres',
        user='postgres',
        password='qwer',
        port='5432')

cur = conn.cursor()

# BUS STOP DB
cur.execute('DROP TABLE IF EXISTS BusStop;')
cur.execute('CREATE TABLE BusStop (id_bus_stop integer PRIMARY KEY,'
                                 'number_people integer NOT NULL,'
                                 'bus_stop_name text NOT NULL,'
                                 'coords text NOT NULL);'
                                 )

# BUS DB
cur.execute('DROP TABLE IF EXISTS Bus;')
cur.execute('CREATE TABLE Bus (id_bus integer PRIMARY KEY,'
                                 'bus_number integer NOT NULL,'
                                 'charge_level text NOT NULL,'
                                 'number_passenger integer NOT NULL);'
                                 )

# DRIVER DB
cur.execute('DROP TABLE IF EXISTS Driver;')
cur.execute('CREATE TABLE Driver (id_driver integer PRIMARY KEY,'
                                 'full_name text NOT NULL,'
                                 'email text NOT NULL,'
                                 'password text NOT NULL,'
                                 'nonstop text NOT NULL);'
                                 )

# ROUTE DB
cur.execute('DROP TABLE IF EXISTS Route;')
cur.execute('CREATE TABLE Route (id_route integer PRIMARY KEY,'
                                 'id_bus_stop integer NOT NULL,'
                                 'serial_num_bustop text NOT NULL);'
                                 )

# BUS TRIP
cur.execute('DROP TABLE IF EXISTS BusTrip;')
cur.execute('CREATE TABLE BusTrip (id_trip integer PRIMARY KEY,'
                                 'id_route integer NOT NULL,'
                                 'id_bus_stop integer NOT NULL,'
                                 'actual_arrival_time time NOT NULL,'
                                 'real_arrival_time time NOT NULL,'
                                 'id_driver integer NOT NULL,'
                                 'id_bus integer NOT NULL);'
                                 )

conn.commit()

cur.close()
conn.close()