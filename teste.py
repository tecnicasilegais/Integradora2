import db_connection
import queries

db = db_connection.Db()

print(db.execute_queries())

