import mysql.connector
from mysql.connector import errorcode
import pandas as pd

# establish a connection to the database
cnx = mysql.connector.connect(host="localhost",
        port="3306",
        user="root",
        password="vcbdac2023",
        database="testdb")

# create a cursor object
cursor = cnx.cursor()

# specify the table name and DataFrame
table_name = 'data_demo'
data_frame = pd.read_csv('data_demo.csv')

# generate the SQL CREATE TABLE statement
columns = list(data_frame.columns)
column_types = ['VARCHAR(255)'] * len(columns)
create_table = f"CREATE TABLE {table_name} ("
for col, col_type in zip(columns, column_types):
    create_table += f"{col} {col_type}, "
create_table = create_table.rstrip(', ')
create_table += ")"
print(create_table)
# execute the CREATE TABLE statement
try:
    cursor.execute(create_table)
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
        print(f"The {table_name} table already exists.")
    else:
        print(err.msg)

# insert the DataFrame into MySQL
for row in data_frame.itertuples():
    insert_data = f"INSERT INTO {table_name} VALUES (" + ','.join(['%s'] * len(columns)) + ")"
    values = tuple(row[1:])
    cursor.execute(insert_data, values)

# commit changes and close connections
cnx.commit()
cursor.close()
cnx.close()
