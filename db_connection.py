import mysql.connector
import os
import time

import queries

USER = os.environ['integradora_user']
PASSWORD = os.environ['integradora_password']


class Db:
    def __init__(self, name):
        self.conn = mysql.connector.connect(user=USER, password=PASSWORD, host='localhost', database='tpch')
        self.cursor = self.conn.cursor()

    def close(self):
        self.cursor.close()
        self.conn.close()

    def execute_queries(self):
        start = time.time()
        for query in enumerate(queries.q):
            self.cursor.execute(query)
        end = time.time()
        return end - start

    def simulate_individual(self, individual):
        return self.execute_queries()
