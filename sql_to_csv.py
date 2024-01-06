import pymysql
import csv

# MySQL Connection Information
host = 'localhost'
user = 'root'
password = ''
database = 'tennis'

# Connect to MySQL
connection = pymysql.connect(host=host, user=user, password=password, database=database)
cursor = connection.cursor()

# Retrieve Table Names
cursor.execute("SHOW TABLES;")
tables = cursor.fetchall()

# Export Tables to CSV
for table in tables:
    table_name = table[0]
    csv_filename = f"{table_name}.csv"

    with open(csv_filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)

        # Retrieve Data from Table
        cursor.execute(f"SELECT * FROM {table_name};")
        table_data = cursor.fetchall()

        # Write Data to CSV
        csv_writer.writerow([i[0] for i in cursor.description])  # Write column headers
        csv_writer.writerows(table_data)  # Write table data to CSV

        print(f"Exported table '{table_name}' to '{csv_filename}'")

# Close Connection
connection.close()
