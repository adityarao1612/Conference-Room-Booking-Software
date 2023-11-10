# check current state of database with all tables and entires listed.
import os
import sqlite3


def print_table_data(connection, table_name):
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()

    print(f"\nTable: {table_name}")
    print("=========================================")
    for row in rows:
        print(row)
    print("=========================================")


def print_all_tables_data(db_file):
    connection = sqlite3.connect(db_file)

    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    print("tables:", tables)
    for table in tables:
        print_table_data(connection, table[0])

    connection.close()


# current_directory = os.getcwd()
# db_file = os.path.join(current_directory, "database.db")
db_file = "conference_app/database/database.db"
print_all_tables_data(db_file)
