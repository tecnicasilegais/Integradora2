import mysql.connector
import os
import time

import queries

USER = os.environ['integradora_user']
PASSWORD = os.environ['integradora_password']
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
