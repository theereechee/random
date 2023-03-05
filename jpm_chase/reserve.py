#!/usr/bin/env python3

"""
This module initializes the plane seats database file (seats.json).
To run this module just execute the python file.
"""

import os.path
import json
import argparse
import initialize_seats_db

seats_db_file = initialize_seats_db.SEATS_DB_FILE


# Handle command line arguments.
def parse_app_args():
    ActionHelp = """
        BOOK = Starts the daemon (default)
        CANCEL = CANCEL reservation(s)
        """

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description="Process plane seat reservations",
    )
    parser.add_argument("action", choices=("BOOK", "CANCEL"), help=ActionHelp)
    parser.add_argument("starting_seat", help="Starting Seat Position e.g A1")
    parser.add_argument(
        "num_seats",
        type=int,
        help="Number of consecutive seats to book (or cancel), from starting seat",
    )

    return parser.parse_args()


# Define functions
def read_seats_db():
    """Reads the seats database from file."""
    if not os.path.isfile(seats_db_file):
        initialize_seats_db.generate_plane_seats()

    with open(seats_db_file, "r") as f:
        seats_db = json.load(f)
    return seats_db


def write_reserved_seats(reserved_seats):
    """Writes the list of reserved seats to file."""
    with open(seats_db_file, "w") as f:
        json.dump(reserved_seats, f, indent=4, sort_keys=True)


def reserve_seats(starting_seat, num_seats):
    """Reserves the given number of seats starting from the given seat."""

    seats_reservation_state = read_seats_db()

    # Check if requested seat parameters are valid
    if not valid_requests(seats_reservation_state, starting_seat, num_seats):
        return False

    row, starting_seat_num = starting_seat[0].upper(), int(starting_seat[1:])
    row_seats = seats_reservation_state.get(row)

    # Fetch the requested seats.
    requested_seats = row_seats[starting_seat_num : starting_seat_num + num_seats]

    # Check if the requested seats are available
    if "BOOKED" in requested_seats:
        return False

    # Reserve the requested seats
    for i in range(starting_seat_num, starting_seat_num + num_seats):
        seats_reservation_state[row][i] = "BOOKED"

    write_reserved_seats(seats_reservation_state)
    return True


def cancel_seats(starting_seat, num_seats):
    """Cancels the reservation of the given number of seats starting from the given seat."""

    seats_reservation_state = read_seats_db()

    # Check if requested seat parameters are valid
    if not valid_requests(seats_reservation_state, starting_seat, num_seats):
        return False

    row, starting_seat_num = starting_seat[0].upper(), int(starting_seat[1:])

    # Cancel the reservation of the requested seats
    for i in range(starting_seat_num, starting_seat_num + num_seats):
        seats_reservation_state[row][i] = ""

    write_reserved_seats(seats_reservation_state)
    return True


def valid_requests(seats_reservation_state, starting_seat, num_seats):
    # check if string length of starting seat complies with seat format.
    if len(starting_seat) < 2:
        return False

    row, starting_seat_num = starting_seat[0].upper(), int(starting_seat[1:])
    row_seats = seats_reservation_state.get(row)

    # Check that the number of seats is positive number and number of seats is not greater than 6 (width of plane)
    if num_seats < 0 or num_seats > 6:
        return False

    # Check if the starting seat number is valid.
    if starting_seat_num not in list(range(6)):
        return False

    # Check if the requested row is available.
    if not row_seats:
        return False

    # Check if the requested number of seats exceeds row capacity from starting seat.
    if starting_seat_num + num_seats > 6:
        return False

    return True


# Main program
def main():
    # Parse command-line arguments
    args = parse_app_args()
    if args.action.upper() == "BOOK":
        success = reserve_seats(args.starting_seat, args.num_seats)
    if args.action.upper() == "CANCEL":
        success = cancel_seats(args.starting_seat, args.num_seats)

    if success:
        print("SUCCESS")
    else:
        print("FAIL")


if __name__ == "__main__":
    main()
