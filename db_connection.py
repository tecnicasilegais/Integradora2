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

err = mysql.connector.errors.ProgrammingError

class Db:
    def __init__(self):
        self.conn = mysql.connector.connect(user=USER, password=PASSWORD, host=HOST, database='tpch',
                                            auth_plugin='mysql_native_password')
        self.cursor = self.conn.cursor()
        self.initial_index_size = self.get_index_size()
        print(self.initial_index_size, type(self.initial_index_size))
        self.last_state = [0] * 22
        self.time_all_indexed = self.simulate_individual([1] * 22)

    def close(self):
        self.cursor.close()
        self.conn.close()

    def clean_cursor(self):
        self.cursor.fetchall()

    def get_index_size(self):
        self.cursor.execute(queries.index_size)
        return self.cursor.fetchone()[0]

    def execute_single_query(self, query):
        self.cursor.execute(query)
        self.clean_cursor()

    def execute_queries(self):
        start = time.time()
        for i in range(1, 15):
            self.execute_single_query(queries.select[i])
            partial_end = time.time()
            print("foi", i, partial_end - start)

        self.cursor.execute(queries.select[15], multi=True)

        for i in range(16, 23):
            self.execute_single_query(queries.select[i])
            partial_end = time.time()
            print("foi", i, partial_end - start)

        end = time.time()
        print(end - start)
        return end - start

    def create_index(self, tbl, column):
        self.cursor.execute(queries.create_index % ('index_' + column, tbl, column))

    def drop_index(self, tbl, column):
        self.cursor.execute(queries.drop_index % ('index_' + column, tbl))

    def rollback(self):
        self.cursor.execute('rollback;')

    def commit(self):
        self.cursor.execute('commit;')

    def debug(self):
        for i in range(22):
            try:
                self.drop_index(INDEXES[i][1], INDEXES[i][0])
            except err as error:
                print(error)
                continue
        print('debug done')

    def simulate_individual(self, individual):
        start = time.time()
        for i in range(len(individual)):
            if self.last_state[i] != individual[i]:
                if individual[i] == 1:
                    self.create_index(INDEXES[i][1], INDEXES[i][0])
                else:
                    self.drop_index(INDEXES[i][1], INDEXES[i][0])
        self.last_state = individual.copy()
        print('time spent creating and dropping indexes:', time.time() - start)

        return self.execute_queries()
