import mysql.connector
import os

USER = os.environ['integradora_user']
PASSWORD = os.environ['integradora_password']

connection = mysql.connector.connect(user=USER, password=PASSWORD, host='localhost', database='tpch')
cursor = connection.cursor()

query = ("SELECT C_MKTSEGMENT FROM tpch.customer where C_CUSTKEY=10;")
cursor.execute(query)

for (c_mktsegments) in cursor:
    print(c_mktsegments)

cursor.close()
connection.close()
