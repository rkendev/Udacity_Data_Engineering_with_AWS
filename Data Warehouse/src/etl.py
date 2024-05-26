import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    """
    Load data from S3 into staging tables in Redshift.

    Parameters:
    - cur: cursor object to execute SQL queries
    - conn: connection object to commit transactions
    """
    for query in copy_table_queries:
        print(f"Executing COPY query: {query}")
        cur.execute(query)
        print(f"Executed COPY query")
        conn.commit()
        print(f"Executed commit for copy")


def insert_tables(cur, conn):
    """
    Insert data from staging tables into the fact and dimension tables in Redshift.

    Parameters:
    - cur: cursor object to execute SQL queries
    - conn: connection object to commit transactions
    """
    for query in insert_table_queries:
        print(f"Executing INSERT query: {query}")
        cur.execute(query)
        print(f"Execute INSERT query")
        conn.commit()
        print(f"Execute commit for INSERT query")


def main():
    """
    Establishes connection to Redshift, loads data into staging tables,
    and inserts data into fact and dimension tables.
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect(
        host=config.get('CLUSTER', 'HOST'),
        dbname=config.get('CLUSTER', 'DB_NAME'),
        user=config.get('CLUSTER', 'DB_USER'),
        password=config.get('CLUSTER', 'DB_PASSWORD'),
        port=config.get('CLUSTER', 'DB_PORT')
    )
    cur = conn.cursor()

    print("Loading staging tables...")
    load_staging_tables(cur, conn)

    print("Inserting data into analytics tables...")
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
