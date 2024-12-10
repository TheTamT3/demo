import json
import logging

from ._constant import successful_booked_msg
from .db import close_connection, create_connection


class Flight:
    def __init__(
            self,
            flight_id: str,
            departure_city: str,
            arrival_city: str,
            departure_date: str,
            arrival_date: str,
            available_economy_seats: int,
            available_business_seats: int,
    ):
        self.flight_id = flight_id
        self.departure_city = departure_city
        self.arrival_city = arrival_city
        self.departure_date = departure_date
        self.arrival_date = arrival_date
        self.available_economy_seats = available_economy_seats
        self.available_business_seats = available_business_seats

    def __str__(self):
        return f"Flight ID: {self.flight_id}, Departure: {self.departure_city}, Arrival: {self.arrival_city}, Departure Date: {self.departure_date}, Arrival Date: {self.arrival_date}, Economy seat: {self.available_economy_seats}, Business seat: {self.available_business_seats}"

    @classmethod
    def get_flight(cls, departure_city, arrival_city, flight_date=None):
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT * FROM flights
                WHERE departure_city = %s AND arrival_city = %s AND DATE(departure_date) = %s
            """,
                (departure_city, arrival_city, flight_date),
            )
            row = cursor.fetchone()
            close_connection(connection)
            if row:
                return cls(*row)
        return []

    @classmethod
    def get_flights(cls, departure_city, arrival_city, flight_date=None):
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            if flight_date:
                cursor.execute(
                    """
                    SELECT * FROM flights
                    WHERE departure_city = %s AND arrival_city = %s AND DATE(departure_date) = %s
                """,
                    (departure_city, arrival_city, flight_date),
                )
            else:
                cursor.execute(
                    """
                    SELECT * FROM flights
                    WHERE departure_city = %s AND arrival_city = %s
                """,
                    (departure_city, arrival_city),
                )
            rows = cursor.fetchall()
            close_connection(connection)
            if rows:
                return [cls(*row) for row in rows]
        return []

    def check_seat_availability(self, seat_economy_count: int = 0, seat_business_count: int = 0) -> bool:
        if seat_economy_count > 0:
            return self.available_economy_seats - seat_economy_count > 0
        if seat_business_count > 0:
            return self.available_business_seats - seat_business_count > 0
        return False


class Booking:
    def __init__(
            self,
            booking_id: str,
            flight_id: str,
            seat_economy_count: int,
            seat_business_count: int,
            user_id: str,
            user_phone_number: str,
    ):
        self.booking_id = booking_id
        self.flight_id = flight_id
        self.seat_economy_count = seat_economy_count
        self.seat_business_count = seat_business_count
        self.user_id = user_id
        self.user_phone_number = user_phone_number

    @classmethod
    def add_booking(
            cls,
            flight: Flight,
            returned_flight: Flight = None,
            seat_economy_count: int = 0,
            seat_business_count: int = 0,
            user_id: str = None,
            user_phone_number: str = None,
    ):
        if not flight.check_seat_availability(seat_economy_count, seat_business_count):
            return "Not enough seat available for departure flight"
        if returned_flight:
            if not returned_flight.check_seat_availability(seat_economy_count, seat_business_count):
                return "Not enough seat available for return flight"

        connection = create_connection()
        if connection:
            metadata = {}
            cursor = connection.cursor()

            if seat_economy_count > 0:
                flight.available_economy_seats -= seat_economy_count
                if returned_flight:
                    returned_flight.available_economy_seats -= seat_economy_count
            if seat_business_count > 0:
                flight.available_business_seats -= seat_business_count
                if returned_flight:
                    returned_flight.available_business_seats -= seat_business_count

            # update available seat
            cursor.execute(
                f"""
                UPDATE flights
                SET available_economy_seats = {flight.available_economy_seats}, available_business_seats = {flight.available_business_seats} WHERE flight_id = {flight.flight_id};
                """
            )
            metadata["user_id"] = user_id
            metadata["user_phone_number"] = user_phone_number
            metadata["one_way_booking"] = {
                "departure_city": flight.departure_city,
                "arrival_city": flight.arrival_city,
                "departure_date": flight.departure_date.strftime('%Y-%m-%d %H:%M:%S'),
                "arrival_date": flight.arrival_date.strftime('%Y-%m-%d %H:%M:%S'),
            }
            if seat_economy_count > 0:
                metadata["one_way_booking"]["seat_economy_count"] = seat_economy_count
            if seat_business_count > 0:
                metadata["one_way_booking"]["seat_business_count"] = seat_business_count

            if returned_flight:
                cursor.execute(
                    f"""
                UPDATE flights
                SET available_economy_seats = {returned_flight.available_economy_seats}, available_business_seats = {returned_flight.available_business_seats} WHERE flight_id = {returned_flight.flight_id};
                """
                )
                metadata["return_flight"] = {
                    "departure_city": returned_flight.departure_city,
                    "arrival_city": returned_flight.arrival_city,
                    "departure_date": returned_flight.departure_date.strftime('%Y-%m-%d %H:%M:%S'),
                    "arrival_date": returned_flight.arrival_date.strftime('%Y-%m-%d %H:%M:%S'),
                }
                if seat_economy_count > 0:
                    metadata["return_flight"]["seat_economy_count"] = seat_economy_count
                if seat_business_count > 0:
                    metadata["return_flight"]["seat_business_count"] = seat_business_count

            # update bookings
            cursor.execute(
                """
                INSERT INTO bookings (flight_id, seat_economy_count, seat_business_count, user_id, user_phone_number)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (flight.flight_id, seat_economy_count, seat_business_count, user_id, user_phone_number),
            )

            if returned_flight:
                cursor.execute(
                    """
                    INSERT INTO bookings (flight_id, seat_economy_count, seat_business_count, user_id, user_phone_number)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (returned_flight.flight_id, seat_economy_count, seat_business_count, user_id, user_phone_number),
                )
            connection.commit()
            close_connection(connection)
            logging.warning(metadata)
            return successful_booked_msg + "\n\n" + json.dumps(metadata)
