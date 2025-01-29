import psycopg2
import json
from psycopg2.extras import execute_values, Json
from datetime import datetime

# Remote Database Connection
remote_conn = psycopg2.connect(
    dbname="recruitment_task",
    user="",
    password="",
    host="recruitment.free.technology",
    port="5432"
)
remote_cursor = remote_conn.cursor()

# Local Database Connection
local_conn = psycopg2.connect(
    dbname="postgres",
    user="admin",
    password="Password",
    host="database",  # Use Docker service name
    port="5432"
)
local_cursor = local_conn.cursor()

# Function to recursively serialize all dicts and datetime objects in a row
def serialize_dicts_and_dates_in_row(row):
    def serialize_value(value):
        if isinstance(value, dict):
            return json.dumps(value)  # Convert dict to JSON string
        elif isinstance(value, list):  
            return json.dumps(value)  # Convert list of dicts to JSON string
        elif isinstance(value, datetime):
            return value.isoformat()  # Convert datetime to ISO string
        return value

    return tuple(serialize_value(value) for value in row)

def sync_tables(schema, tables):

    for table in tables:
        print(f"Syncing table: {table}...")

        # Fetch data and column names from remote
        remote_cursor.execute(f"SELECT * FROM {schema}.{table} LIMIT 1;")
        column_names = [desc[0] for desc in remote_cursor.description]

        # Check if table exists
        local_cursor.execute(f"SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = '{table}');")
        table_exists = local_cursor.fetchone()[0]

        # Create table if it does not exist
        if not table_exists:
            print(f"Table {table} does not exist. Creating...")
            remote_cursor.execute(f"""
                SELECT column_name, data_type FROM information_schema.columns 
                WHERE table_schema = '{schema}' AND table_name = '{table}';
            """)
            columns = remote_cursor.fetchall()

            column_definitions = ", ".join([f'"{col[0]}" {col[1]}' for col in columns])
            create_table_query = f'CREATE TABLE public."{table}" ({column_definitions});'
            local_cursor.execute(create_table_query)
            print(f"Table {table} created.")

        # Truncate local table before inserting new data
        local_cursor.execute(f'TRUNCATE TABLE public."{table}" RESTART IDENTITY;')

        # Fetch all data after ensuring the table exists
        remote_cursor.execute(f"SELECT * FROM {schema}.{table};")
        data = remote_cursor.fetchall()

        # Serialize dict values and datetime objects in the data
        data = [serialize_dicts_and_dates_in_row(row) for row in data]

        column_names_escaped = ', '.join([f'"{col}"' for col in column_names])
        # Insert data into local PostgreSQL
        insert_query = 'INSERT INTO public."{}" ({}) VALUES %s'.format(table, column_names_escaped)
        try:
            execute_values(local_cursor, insert_query, data)
        except Exception as e:
            print(f"Error inserting data into table {table}: {e}")
            raise

        print(f"Table {table} synced.")

# Syncing tables
sync_tables('raw_github', ["issues", "commits", "pull_requests", "repositories"])
sync_tables('raw_finance', ["invoice"])

# Commit changes
local_conn.commit()
remote_conn.close()
local_conn.close()
