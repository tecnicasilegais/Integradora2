import mysql.connector
import os
import time

import queries

USER = os.environ['integradora_user']
PASSWORD = os.environ['integradora_password']
HOST = os.environ['integradora_host']
INDEXES = {
    0: ["c_phone", "customer"], 1: ["c_acctbal", "customer"], 2: ["c_mktsegment", "customer"],
    3: ["o_orderstatus", "orders"], 4: ["o_orderdate", "orders"], 5: ["o_comment", "orders"],
    6: ["ps_availqty", "partsupp"], 7: ["ps_supplycost", "partsupp"], 8: ["p_name", "part"], 9: ["p_brand", "part"],
    10: ["p_type", "part"], 11: ["p_size", "part"], 12: ["p_container", "part"], 13: ["l_linenumber", "lineitem"],
    14: ["l_returnflag", "lineitem"], 15: ["l_discount", "lineitem"], 16: ["l_shipdate", "lineitem"],
    17: ["l_commitdate", "lineitem"], 18: ["l_receiptdate", "lineitem"], 19: ["l_shipinstruct", "lineitem"],
    20: ["l_shipmode", "lineitem"], 21: ["l_quantity", "lineitem"]
}


class Db:
    def __init__(self):
        self.conn = mysql.connector.connect(user=USER, password=PASSWORD, host=HOST, database='tpch',
                                            auth_plugin='mysql_native_password')
        self.cursor = self.conn.cursor()
        self.initial_index_size = self.get_index_size()
        self.last_state = [0] * 22

    def close(self):
        self.cursor.close()
        self.conn.close()

    def clean_cursor(self):
        self.cursor.fetchall()

    def get_index_size(self):
        self.cursor.execute(queries.index_size)
        return self.cursor.fetchone()

    def execute_queries(self):
        start = time.time()
        for i in range(1, 23):
            self.cursor.execute(queries.select[i])
            self.clean_cursor()
            print("foi", i)
        end = time.time()
        return end - start

    def create_index(self, tbl, column):
        self.cursor.execute(queries.create_index, (column, tbl))

    def drop_index(self, tbl, column):
        self.cursor.execute(queries.drop_index, (column, tbl))

    def simulate_individual(self, individual):
        for i in range(len(individual)):
            if self.last_state[i] != individual[i]:
                if individual[i] == 1:
                    self.create_index(INDEXES[i][1], INDEXES[i][0])
                else:
                    self.drop_index(INDEXES[i][1], INDEXES[i][0])

        return self.execute_queries()
