import psycopg2
from psycopg2 import OperationalError
import os



DB_ENDPOINT = os.getenv('RDS_ENDPOINT')
DB_USER = os.getenv('RDS_USER')
DB_PASSWORD = os.getenv('RDS_PASSWORD')
DB_PORT = os.getenv('RDS_PORT')
DB_NAME = os.getenv('RDS_DBNAME')

def create_connection(DB_ENDPOINT, DB_USER, DB_PASSWORD, DB_PORT, DB_NAME):
    """
    Create a database connection to a PostgreSQL database
    """
    conn = None
    try:
        conn = psycopg2.connect(
            host=DB_ENDPOINT,
            user=DB_USER,
            password=DB_PASSWORD,
            dbname=DB_NAME,
            port=DB_PORT
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return conn

if __name__ == '__main__':
    POSTGRES_HOST = "localhost"
    POSTGRES_USER = "airflow"
    POSTGRES_PASSWORD = "airflow"
    POSTGRES_NAME = "airflow"
    POSTGRES_PORT = 5432
    # conn = create_connection(DB_ENDPOINT, DB_USER, DB_PASSWORD, DB_PORT)
    conn = create_connection(POSTGRES_HOST, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_PORT, POSTGRES_NAME)
    if conn:
        # execute sql
        with conn.cursor() as cur:
            cur.execute("SELECT datname FROM pg_database;")
            db_list = cur.fetchall()

        print([db[0] for db in db_list])

    
