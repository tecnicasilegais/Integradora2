import mysql.connector
import os

import queries

USER = os.environ['integradora_user']
PASSWORD = os.environ['integradora_password']

connection = mysql.connector.connect(user=USER, password=PASSWORD, host='localhost', database='tpch')
cursor = connection.cursor()

for query in enumerate(queries.q):
    cursor.execute(query)

cursor.close()
connection.close()
