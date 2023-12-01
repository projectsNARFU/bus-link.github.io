import psycopg2
from initalization_databases import get_db_connection

def insert_busstop(number_people, bus_stop_name, coords):
    conn = get_db_connection()

    cur = conn.cursor()

    cur.execute("""
                INSERT INTO bus_stop (number_people, bus_stop_name, coords)
                VALUES (%s, %s, %s)
                """, (number_people, bus_stop_name, coords))
    
    conn.commit()

    cur.close()
    conn.close()

def insert_driver(full_name, email, password):
    conn = get_db_connection()

    cur = conn.cursor()

    cur.execute("""
                INSERT INTO driver (full_name, email, password)
                VALUES (%s, %s, %s)
                """, (full_name, email, password))
    
    conn.commit()

    cur.close()
    conn.close()

def insert_bus(bus_number):

    conn = get_db_connection()

    cur = conn.cursor()

    cur.execute("""
                INSERT INTO bus (bus_number)
                VALUES (%s)
                """, (bus_number,))
    
    conn.commit()

    cur.close()
    conn.close()

def insert_route(id_route, id_bus_stop, serial_num_bustop):
    
    conn = get_db_connection()

    cur = conn.cursor()

    cur.execute("""
                INSERT INTO route (id_route, id_bus_stop, serial_num_bustop)
                VALUES (%s, %s, %s)
                """, (id_route, id_bus_stop, serial_num_bustop))
    
    conn.commit()

    cur.close()
    conn.close()

def insert_bus_trip(id_trip, id_route, id_bus_stop, 
                    actual_arrival_time, id_driver, id_bus):

    conn = get_db_connection()

    cur = conn.cursor()

    cur.execute("""
                INSERT INTO bus_trip (id_trip, id_route, id_bus_stop, 
                    actual_arrival_time, real_arrival_time, id_driver, id_bus)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (id_trip, id_route, id_bus_stop,
                        actual_arrival_time, actual_arrival_time,
                        id_driver, id_bus))
    
    conn.commit()

    cur.close()
    conn.close()

def add_new_route(list_bus_stop):
    
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
                SELECT MAX(id_route)
                FROM route
                """)
    old_max_id = cur.fetchone()
    print(old_max_id[0])


    cur.close()
    conn.close()

if __name__ == '__main__':
    # insert_busstop(1, 'zayats', '100.8.8')
    # insert_busstop(10, 'volk', '112.75.82')
    # insert_busstop(6, 'tigr', '133.72.81')
    # insert_busstop(7, 'sobaka', '150.2.1')

    # insert_driver('ivanov ivan ivanovich', 
    #             'ivanovich1980@mail.ru', 'qwerty')
    
    # insert_bus(42)
    
    # insert_route(1, 3, 1)
    # insert_route(1, 1, 2)
    # insert_route(1, 2, 3)
    # insert_route(1, 4, 4)

    # insert_bus_trip(1, 1, 3, '8:00', 1, 1)
    # insert_bus_trip(1, 1, 1, '8:10', 1, 1)
    # insert_bus_trip(1, 1, 2, '8:20', 1, 1)
    # insert_bus_trip(1, 1, 4, '8:30', 1, 1)
    add_new_route([3, 1, 2, 4])
    pass