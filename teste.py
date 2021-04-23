import time

import db_connection
import numpy as np

db = db_connection.Db()

# db.debug()

start = time.time()
for i in range(0, 5000):
    individual = np.random.randint(2, size=22)
    db.simulate_individual(individual)
    print(i)

end = time.time()
print(end - start)
db.close()
