import mysql.connector
import os
import time

import queries

USER = os.environ['integradora_user']
PASSWORD = os.environ['integradora_password']

connection = mysql.connector.connect(user=USER, password=PASSWORD, host='localhost', database='tpch')
cursor = connection.cursor()


def execute_queries():
    start = time.time()
    for query in enumerate(queries.q):
        cursor.execute(query)
    end = time.time()
    return end - start


def simulate_individual(individual):
    execute_queries()


cursor.close()
connection.close()
