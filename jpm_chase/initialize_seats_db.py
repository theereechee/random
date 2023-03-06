#!/usr/bin/env python3

"""
This module initializes the plane seats database file (seats.json).
To run this module just execute the python file.
"""

import json
import string


SEATS_DB_FILE = "seats.json"
PLANE_SEAT_WIDTH = 8
NUM_ROWS = 20
SEATS_DB = {}


def generate_plane_seats():
    """Generate plane seats based on specifications in requirements file"""
    for row in string.ascii_uppercase[:NUM_ROWS]:
        SEATS_DB[row] = ["" for i in range(PLANE_SEAT_WIDTH)]

    with open(SEATS_DB_FILE, "w") as f:
        json.dump(SEATS_DB, f, indent=4, sort_keys=True)


if __name__ == "__main__":
    generate_plane_seats()
