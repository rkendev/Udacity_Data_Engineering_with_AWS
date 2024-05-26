# Sparkify Data Warehouse

## Introduction
Sparkify is a startup company that provides a music streaming service. The purpose of this project is to build a data warehouse that will help Sparkify analyze their user activity data to gain insights into user behaviors and preferences. By leveraging this data, Sparkify can make data-driven decisions to improve user experience, optimize their content offerings, and drive user engagement.

## Database Schema Design
The database schema for the Sparkify data warehouse follows a star schema design, which is optimized for complex queries and aggregations. The star schema consists of fact and dimension tables:

### Fact Table
- **songplays** - records in event data associated with song plays
  - songplay_id (BIGINT) PRIMARY KEY
  - start_time (TIMESTAMP) NOT NULL
  - user_id (INT) NOT NULL
  - level (VARCHAR)
  - song_id (VARCHAR)
  - artist_id (VARCHAR)
  - session_id (BIGINT)
  - location (VARCHAR)
  - user_agent (TEXT)

### Dimension Tables
- **users** - users in the app
  - user_id (INT) PRIMARY KEY
  - first_name (VARCHAR)
  - last_name (VARCHAR)
  - gender (VARCHAR)
  - level (VARCHAR)

- **songs** - songs in music database
  - song_id (VARCHAR) PRIMARY KEY
  - title (VARCHAR)
  - artist_id (VARCHAR)
  - year (INT)
  - duration (DOUBLE PRECISION)

- **artists** - artists in music database
  - artist_id (VARCHAR) PRIMARY KEY
  - name (VARCHAR)
  - location (VARCHAR)
  - latitude (DOUBLE PRECISION)
  - longitude (DOUBLE PRECISION)

- **time** - timestamps of records in songplays broken down into specific units
  - start_time (TIMESTAMP) PRIMARY KEY
  - hour (INT)
  - day (INT)
  - week (INT)
  - month (INT)
  - year (INT)
  - weekday (INT)

### Justification
The star schema is chosen for its simplicity and efficiency in querying large datasets. Fact tables contain the metrics of the business processes (song plays), and dimension tables store the context (user details, song details, artist details, and time details) to allow for easy and performant querying.

## ETL Pipeline
The ETL (Extract, Transform, Load) pipeline extracts data from JSON log files stored in an S3 bucket, transforms it into a format suitable for analysis, and loads it into the Redshift data warehouse. The steps involved in the ETL pipeline are as follows:

1. **Extract**: 
   - Load the data from the S3 bucket into staging tables in Redshift.
   - `staging_events` table for event data.
   - `staging_songs` table for song data.

2. **Transform**:
   - Process the staging tables to create the fact and dimension tables.
   - Clean and format the data as needed.

3. **Load**:
   - Insert the transformed data into the fact and dimension tables in Redshift.

### ETL Process Steps
1. **Load Staging Tables**: 
   - Copy data from the S3 bucket to the `staging_events` and `staging_songs` tables in Redshift using the `COPY` command.

2. **Insert Data into Fact and Dimension Tables**:
   - Transform and load data from the staging tables into the fact and dimension tables using `INSERT INTO` SELECT statements.

### Data Warehouse Folder Structure
- **create_tables.py**: Python script to create the necessary tables in Redshift.
- **etl.py**: Python script to extract data from S3, transform it, and load it into Redshift.
- **sql_queries.py**: Contains SQL queries for creating, dropping tables, and inserting data.
- **dwh.cfg**: Configuration file containing AWS and Redshift cluster details.
- **README.md**: Documentation for the Data Warehouse project.

## How to Run the Python Scripts
To run the ETL pipeline and set up the database, follow these steps:

1. **Clone the repository**:
   ```sh
   git clone <repository_url>
   cd <repository_directory>```

2. **Configure the dwh.cfg file**
Update the dwh.cfg file with your AWS and Redshift cluster details:

    ```[CLUSTER]
    HOST=<your_redshift_cluster_endpoint>
    DB_NAME=<your_database_name>
    DB_USER=<your_database_user>
    DB_PASSWORD=<your_database_password>
    DB_PORT=5439
    
    [IAM_ROLE]
    ARN=<your_iam_role_arn>
    
    [S3]
    LOG_DATA=<your_log_data_s3_path>
    LOG_JSONPATH=<your_log_jsonpath_s3_path>
    SONG_DATA=<your_song_data_s3_path>
    
    [REGION]
    AWS_BUCKET_REGION=<your_s3_bucket_region>

3. **Create the database tables**
Run the create_tables.py script to create the necessary tables in the Redshift cluster: **python create_tables.py**

4. **Run the ETL pipeline**
Execute the etl.py script to load data from S3 into the Redshift tables: **python etl.py**

## Example Queries
        SELECT 
            users.user_id,
            users.first_name,
            users.last_name,
            COUNT(songplays.session_id) AS session_count
        FROM songplays
        JOIN users ON songplays.user_id = users.user_id
        GROUP BY users.user_id, users.first_name, users.last_name
        ORDER BY session_count DESC
        LIMIT 10;

    
        SELECT 
            songs.title AS song_title,
            artists.name AS artist_name,
            SUM(songs.duration) AS total_playtime
        FROM songplays
        JOIN songs ON songplays.song_id = songs.song_id
        JOIN artists ON songplays.artist_id = artists.artist_id
        GROUP BY songs.title, artists.name
        ORDER BY total_playtime DESC
        LIMIT 10;
        
        SELECT 
            location,
            COUNT(*) AS play_count
        FROM songplays
        GROUP BY location
        ORDER BY play_count DESC
        LIMIT 10;

More queries can be found in the queries_for_validation folder

