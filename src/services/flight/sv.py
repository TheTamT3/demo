import logging

from ._constant import not_found_departure_flight_msg, not_found_return_flight_msg, system_error_msg
from .models import Booking, Flight


def book_flight(
    departure_city: str,
    arrival_city: str,
    departure_date: str,
    user_id: str,
    user_phone_number: str,
    seat_economy_count: int = 0,
    seat_business_count: int = 0,
    arrival_date: str | None = None,
):
    try:
        flight = Flight.get_flight(departure_city, arrival_city, departure_date)

        if not flight:
            return not_found_departure_flight_msg.format(departure_city=departure_city, arrival_city=arrival_city)

        returned_flight = None
        if arrival_date:
            returned_flight = Flight.get_flight(arrival_city, departure_city, arrival_date)
            if not returned_flight:
                return not_found_return_flight_msg.format(departure_city=arrival_city, arrival_city=departure_city)

        result = Booking.add_booking(
            flight=flight,
            returned_flight=returned_flight,
            seat_economy_count=seat_economy_count,
            seat_business_count=seat_business_count,
            user_id=user_id,
            user_phone_number=user_phone_number,
        )
        return result
    except Exception as e:
        logging.error(e)
        return system_error_msg


def get_flights(departure_city: str, arrival_city: str, departure_date: str = None) -> str:
    try:
        flights = Flight.get_flights(departure_city, arrival_city, departure_date)
        output = ""
        for flight in flights:
            output += f"{flight.__str__()}\n"
        return output
    except Exception as e:
        logging.error(e)
        return system_error_msg
