import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def drop_tables(cur, conn):
    """
    Drop all existing tables in Redshift.

    Parameters:
    - cur: cursor object to execute SQL queries
    - conn: connection object to commit transactions
    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """
    Create tables in Redshift.

    Parameters:
    - cur: cursor object to execute SQL queries
    - conn: connection object to commit transactions
    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    Establishes connection to Redshift, drops existing tables,
    and creates new tables as defined in the SQL queries.
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    try:
        conn = psycopg2.connect(
            host=config.get('CLUSTER', 'HOST'),
            dbname=config.get('CLUSTER', 'DB_NAME'),
            user=config.get('CLUSTER', 'DB_USER'),
            password=config.get('CLUSTER', 'DB_PASSWORD'),
            port=config.get('CLUSTER', 'DB_PORT')
        )
        cur = conn.cursor()
        print("Connected to the database successfully.")
    except Exception as e:
        print("Error: Could not make connection to the Redshift cluster.")
        print(e)
        return

    try:
        drop_tables(cur, conn)
        create_tables(cur, conn)
        print("Tables dropped and created successfully.")
    except Exception as e:
        print("Error: Issue encountered while dropping or creating tables.")
        print(e)
    finally:
        conn.close()
        print("Connection closed.")


if __name__ == "__main__":
    main()
