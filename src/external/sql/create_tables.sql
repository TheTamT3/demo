CREATE TABLE flights (
    flight_id INT AUTO_INCREMENT PRIMARY KEY,
    departure_city VARCHAR(100) NOT NULL,
    arrival_city VARCHAR(100) NOT NULL,
    departure_date DATETIME NOT NULL,
    arrival_date DATETIME NOT NULL,
    available_economy_seats INT NOT NULL,
    available_business_seats INT NOT NULL
);


CREATE TABLE bookings (
    booking_id INT AUTO_INCREMENT PRIMARY KEY,
    flight_id INT NOT NULL,
    seat_economy_count INT DEFAULT 0,
    seat_business_count INT DEFAULT 0,
    user_id INT NOT NULL,
    user_phone_number VARCHAR(20) NOT NULL
);
