"""
    author: sahalajosuasinaga@gmail.com
"""

import sqlite3
import os
from dotenv import load_dotenv #type: ignore
from . transform import TransformData



class LoadData:

    def load_data(self):
        # Define the database path
        load_dotenv()
        
        DB_PATH = os.environ['db_conn']

        # Check if the directory exists, if not, create it
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

        # Connect to the database (it will be created if it does not exist)
        try:
            conn = sqlite3.connect(DB_PATH)
            print(f"Database '{DB_PATH}' created successfully or already exists.")

            LoadData.create_table(conn)

            transform_data = TransformData()
            LoadData.insert_to_table(conn, transform_data)
            LoadData.select_all_from_table(conn)

        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        finally:
            if conn:
                conn.close()


    def create_table(conn):

        create_table_sql = """
        CREATE TABLE IF NOT EXISTS born_date_data (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            phone_number TEXT NOT NULL,
            born_day DATE NOT NULL
        );
        """

        cursor = conn.cursor()
        cursor.execute(create_table_sql)
        print("Table 'born_date_data' created successfully or already exists.")

        conn.commit()


    def insert_to_table(conn, transform_data):
        # Retrieve data from Google Sheets
        read_data = transform_data.convert_to_dataframe()  # Adjust if 'self' is necessary

        cursor = conn.cursor()
        
        # Truncate (delete all rows) from the table
        try:
            cursor.execute("DELETE FROM born_date_data")
            print("Table 'born_date_data' truncated successfully.")
        except sqlite3.Error as e:
            print(f"An error occurred while truncating table: {e}")


        # Prepare the insert SQL statement
        insert_sql = """
        INSERT INTO born_date_data (id, name, phone_number, born_day)
        VALUES (?, ?, ?, ?)
        """
        
        # Check if read_data is empty
        if read_data is not None and len(read_data) > 0:
            # Iterate over the DataFrame and insert each row
            for _, row in read_data.iterrows():
                try:
                    cursor.execute(insert_sql, (row['id'], row['name'], row['phone_number'], row['born_day']))
                except sqlite3.Error as e:
                    print(f"An error occurred while inserting data: {e}")

            print(f"Inserted {len(read_data)} rows into 'born_date_data'.")
        else:
            print("No data retrieved to insert.")

        conn.commit()


    def select_all_from_table(conn):
        cursor = conn.cursor()
        
        # Execute a SELECT statement
        cursor.execute("SELECT * FROM born_date_data")
        
        # Fetch all rows from the executed query
        rows = cursor.fetchall()

        # Print the results
        print("Data from 'born_date_data':")
        for row in rows:
            print(row)