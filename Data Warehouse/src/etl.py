import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    for query in copy_table_queries:
        print(f"Executing COPY query: {query}")
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    for query in insert_table_queries:
        print(f"Executing INSERT query: {query}")
        cur.execute(query)
        conn.commit()


def get_table_counts(cur):
    tables = ['staging_events', 'staging_songs', 'songplays', 'users', 'songs', 'artists', 'time']
    counts = {}
    for table in tables:
        cur.execute(f"SELECT COUNT(*) FROM {table}")
        counts[table] = cur.fetchone()[0]
    return counts


def main():
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

    print("Fetching counts from tables to validate the ETL process...")
    counts = get_table_counts(cur)

    for table, count in counts.items():
        print(f"SELECT COUNT(*) FROM {table} [{count}]")

    conn.close()


if __name__ == "__main__":
    main()
