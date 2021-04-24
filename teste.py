import db_connection
import logging

import util

logging.basicConfig(filename=util.make_filename('gen_execution.log'), encoding='utf-8', level=logging.DEBUG)

db = db_connection.Db(logging)

individual = [0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0]
individual2 = [0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0]
db.simulate_individual(individual)
db.simulate_individual(individual2)

db.close()
