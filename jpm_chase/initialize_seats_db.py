"""
This module initializes the plane seats database file (seats.json).
To run this module just execute the python file.
"""

import json
import string


SEATS_DB_FILE = "seats.json"
NUM_ROWS = 20
seats_db = {}


def generate_plane_seats():
    """Generate plane seats based on specifications in requirements file"""
    for row in string.ascii_uppercase[:NUM_ROWS]:
        seats_db[row] = ["" for i in range(6)]

    with open(SEATS_DB_FILE, "w") as f:
        json.dump(seats_db, f, indent=4, sort_keys=True)


if __name__ == "__main__":
    generate_plane_seats()
