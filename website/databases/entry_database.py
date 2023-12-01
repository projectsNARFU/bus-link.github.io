import psycopg2
from initalization_databases import get_db_connection

def insert_busstop(id_bus_stop, number_people, bus_stop_name, coords):
    conn = get_db_connection()

    cur = conn.cursor()

    cur.execute("""
                INSERT INTO bus_stop (number_people, bus_stop_name, coords)
                VALUES (%s, %s, %s)
                """, (number_people, bus_stop_name, coords))
    
    conn.commit()

    cur.close()
    conn.close()

if __name__ == '__main__':
    """
    проверка что вводимые ключи уникальные
    вообще я думаю, что id будет автоматически вводиться, 
    руководитель не должен париться на этот счет,
    хотя тут уже вопрос успеем ли мы
    """
    insert_busstop(10, 'vorona', '123.3214.7')