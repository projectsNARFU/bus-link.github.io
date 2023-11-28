from ast import main
import psycopg2

def get_db_connection():
    conn = psycopg2.connect(
            host='localhost',
            dbname='postgres',
            user='postgres',
            password='qwer',
            port='5432')
    return conn


def initialization_db():
    conn = get_db_connection()

    cur = conn.cursor()

    cur.execute('DROP TABLE IF EXISTS drivers;')
    cur.execute('CREATE TABLE drivers (id serial PRIMARY KEY,'
                                    'name varchar (150) NOT NULL,'
                                    'number_bus INT NOT NULL);'
                                    )


    cur.execute('INSERT INTO drivers (name, number_bus)'
                'VALUES (%s, %s)',
                ('Иванов Иван Иванович',
                42)
                )


    cur.execute('INSERT INTO drivers (name, number_bus)'
                'VALUES (%s, %s)',
                ('Петров Михаил Дмитриевич',
                43)
                )

    conn.commit()

    cur.close()
    conn.close()


if __name__ == '__main__':
    initialization_db()