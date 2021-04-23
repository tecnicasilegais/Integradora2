import db_connection
import queries

db = db_connection.Db()

db.simulate_individual([0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0])

db.close()
