import mysql.connector
import os
import time

import queries

USER = os.environ['integradora_user']
PASSWORD = os.environ['integradora_password']


class Db:
    def __init__(self, name):
        self.conn = mysql.connector.connect(user=USER, password=PASSWORD, host='localhost', database='tpch')
        self.cursor = self.conn.cursor
        self.initial_index_size = self.get_index_size()
        self.biggest_tables = self.get_biggest_tables()

    def close(self):
        self.cursor.close()
        self.conn.close()

    def get_biggest_tables(self):
        self.cursor.execute('todo')
        return self.cursor.biggest

    def get_index_size(self):
        self.cursor.execute(queries.index_size)
        return self.cursor.index_size

    def execute_queries(self):
        start = time.time()
        for query in queries.select:
            self.cursor.execute(query)
        end = time.time()
        return end - start

    def simulate_individual(self, individual):
        return self.execute_queries()
