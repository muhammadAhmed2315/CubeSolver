from cube import Cube
from solver import IDA_star
import os
import json
import time

HEURISTIC_FILE = 'heuristic.json'
REGENERATE_HEURISTIC_DB = False

cube = Cube()

# if heuristic file already exists, assign it to heuristic_db
if os.path.exists(HEURISTIC_FILE):
    with open(HEURISTIC_FILE) as file:
        heuristic_db = json.load(file)
else:
    heuristic_db = None

# if no heuristic file exists or user wants to regenerate the database
if heuristic_db is None or REGENERATE_HEURISTIC_DB is True:
    heuristic_db = cube.build_heuristic_db()
    with open(HEURISTIC_FILE, 'w', encoding='utf-8') as f:
        json.dump(
            heuristic_db,
            f,
            ensure_ascii=False,
            indent=4
        )

print(cube.scramble(10))
solver = IDA_star(heuristic_db)
cube.visualise()

temp_time = time.time()
moves = solver.run(cube.state)
print(f"Rotations: {time.time() - temp_time}")
print(moves)

# applies algorithm to the cube
cube.apply_algorithm(moves)
cube.visualise()
