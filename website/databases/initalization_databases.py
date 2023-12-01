import psycopg2

def get_db_connection():
    conn = psycopg2.connect(
            host='localhost',
            dbname='postgres',
            user='postgres',
            password='qwer',
            port='5432')
    return conn

def initialize_databases():
    conn = get_db_connection()

    cur = conn.cursor()

    # # BUS STOP DB
    # cur.execute('DROP TABLE IF EXISTS bus_stop;')
    # cur.execute('CREATE TABLE bus_stop (id_bus_stop serial PRIMARY KEY,'
    #                                 'number_people integer NOT NULL,'
    #                                 'bus_stop_name text NOT NULL,'
    #                                 'coords text NOT NULL UNIQUE);'
    #                                 )

    # # BUS DB
    # cur.execute('DROP TABLE IF EXISTS bus;')
    # cur.execute('CREATE TABLE bus (id_bus serial PRIMARY KEY,'
    #                                 'bus_number integer NOT NULL,'
    #                                 'charge_level text NOT NULL DEFAULT 0,'
    #                                 'number_passenger integer NOT NULL DEFAULT 0);'
    #                                 )

    # # DRIVER DB
    # cur.execute('DROP TABLE IF EXISTS driver;')
    # cur.execute('CREATE TABLE driver (id_driver serial PRIMARY KEY,'
    #                                 'full_name text NOT NULL,'
    #                                 'email text NOT NULL UNIQUE,'
    #                                 'password text NOT NULL,'
    #                                 'nonstop text DEFAULT 0);'
    #                                 )

    # # ROUTE DB
    # cur.execute('DROP TABLE IF EXISTS route;')
    # cur.execute("""CREATE TABLE route (
    #             id_route integer,
    #             id_bus_stop integer NOT NULL,
    #             serial_num_bustop integer NOT NULL,
    #             PRIMARY KEY (id_route, id_bus_stop),
    #             FOREIGN KEY (id_bus_stop) REFERENCES bus_stop (id_bus_stop)
    #             );
    #             """)

    # BUS TRIP
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
    
    # GLOBAL CONDITIONS
    cur.execute('DROP TABLE IF EXISTS global_conditions;')
    cur.execute('CREATE TABLE global_conditions (current_weather integer PRIMARY KEY,'
                                    'date_now date DEFAULT current_date,'
                                    'time_now time DEFAULT current_time,'
                                    'fiesta boolean DEFAULT false);'
                                    )

    conn.commit()

    cur.close()
    conn.close()

if __name__ == '__main__':
    initialize_databases()