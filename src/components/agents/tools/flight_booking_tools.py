tools = [
    {
        "type": "function",
        "function": {
            "name": "book_flight",
            "parameters": {
                "type": "object",
                "properties": {
                    "departure_city": {"type": "string"},
                    "arrival_city": {"type": "string"},
                    "departure_date": {"type": "string", "format": "date"},
                    "arrival_date": {"type": "string", "format": "date"},
                    "seat_economy_count": {"type": "integer"},
                    "seat_business_count": {"type": "integer"},
                    "user_id": {"type": "string", "description": "customer's identification number"},
                    "user_phone_number": {"type": "string", "description": "customer's phone number"},
                },
                "required": ["departure_city", "arrival_city", "departure_date", "seat_class", "seat_count", "user_id", "user_phone_number"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_flights",
            "parameters": {
                "type": "object",
                "properties": {
                    "departure_city": {"type": "string"},
                    "arrival_city": {"type": "string"},
                    "departure_date": {"type": "string", "format": "date"},
                },
                "required": ["departure_city", "arrival_city"],
                "additionalProperties": False,
            },
        },
    }
]
