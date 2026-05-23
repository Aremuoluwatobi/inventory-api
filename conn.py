import psycopg2


def get_connection():
    connection = psycopg2.connect(
        host="localhost",
        database="inventory_db",
        user="postgres",
        password="0707"
    )

    return connection
