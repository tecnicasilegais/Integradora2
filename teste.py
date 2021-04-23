import db_connection
import numpy as np

db = db_connection.Db()

# db.debug()

for i in range(0, 5000):
    individual = np.random.randint(2, size=22)
    db.simulate_individual(individual)
    print(i)

db.close()
