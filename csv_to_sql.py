import pymysql
import os
import csv

# MySQL Connection Information
host = 'localhost'
user = 'zoe_nathan'
password = 'zoe_nathan'
database = 'tennis'

# Directory containing CSV files
csv_directory = 'csv_files'

# Connect to MySQL
connection = pymysql.connect(host=host, user=user, password=password)
cursor = connection.cursor()

# Create 'tennis' database
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database};")
cursor.execute(f"USE {database};")

# Get list of CSV files in the directory
csv_files = [file for file in os.listdir(csv_directory) if file.endswith('.csv')]

# Import CSV files to MySQL as tables
for file in csv_files:
    table_name = os.path.splitext(file)[0]  # Use filename as table name

    with open(os.path.join(csv_directory, file), 'r') as csvfile:
        csv_data = csv.reader(csvfile)
        headers = next(csv_data)  # Extract headers

        # Create table in the database
        columns = ', '.join(f"`{header.strip()}` VARCHAR(255)" for header in headers)
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns});"
        cursor.execute(create_table_query)

        # Insert data into the table
        insert_query = f"INSERT INTO {table_name} ({', '.join(headers)}) VALUES ({', '.join(['%s'] * len(headers))})"
        for row in csv_data:
            cursor.execute(insert_query, row)

    print(f"Imported '{file}' as table '{table_name}'")

# Commit changes and close connection
connection.commit()
connection.close()
