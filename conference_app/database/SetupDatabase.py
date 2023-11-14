# RUN THIS FILE TO RESET THE DATABASE AND  POPULATE IT WITH SAMPLE DATA

import sqlite3
from sqlite3 import Error
import pandas as pd


def create_connection(db_file):
    connection = None
    try:
        connection = sqlite3.connect(db_file)
        print("SQLite Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection


db_file = "conference_app/database/database.db"

# Use SQLite and create a connection to the database file
connection = create_connection(db_file)

cursor = connection.cursor()

# Define the database name
database_name = 'conference_room_booking'

try:
    # Drop the table if it already exists
    cursor.execute(f"DROP TABLE IF EXISTS Users")
    cursor.execute(f"DROP TABLE IF EXISTS Rooms")
    cursor.execute(f"DROP TABLE IF EXISTS BookedRoom")
    cursor.execute(f"DROP TABLE IF EXISTS WaitingList")
    cursor.execute(f"DROP TABLE IF EXISTS Notifications")

    # Create the tables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        email TEXT NOT NULL,
        full_name TEXT,
        user_type TEXT CHECK(user_type IN ('admin', 'regular', 'room owner')) NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Rooms (
        room_id INTEGER PRIMARY KEY AUTOINCREMENT,
        room_name TEXT NOT NULL,
        capacity INTEGER NOT NULL,
        projector INTEGER NOT NULL,
        mics INTEGER NOT NULL,
        whiteboard INTEGER NOT NULL,
        price DECIMAL(10, 2),
        location TEXT,
        description TEXT,
        availability TEXT CHECK(availability IN ('available', 'unavailable')) NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS BookedRoom (
        booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        room_id INTEGER,
        start_datetime DATETIME,
        end_datetime DATETIME,
        purpose TEXT,
        status TEXT CHECK(status IN ('confirmed', 'pending', 'canceled')) NOT NULL,
        FOREIGN KEY (user_id) REFERENCES Users(user_id),
        FOREIGN KEY (room_id) REFERENCES Rooms(room_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS WaitingList (
        waiting_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        room_id INTEGER,
        requested_datetime DATETIME,
        status TEXT CHECK(status IN ('pending', 'approved', 'declined')) NOT NULL,
        FOREIGN KEY (user_id) REFERENCES Users(user_id),
        FOREIGN KEY (room_id) REFERENCES Rooms(room_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Notifications (
        notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        message TEXT,
        timestamp DATETIME,
        status TEXT CHECK(status IN ('unread', 'read')) NOT NULL,
        FOREIGN KEY (user_id) REFERENCES Users(user_id)
    )
    """)

    cursor.execute("""
    CREATE TRIGGER IF NOT EXISTS update_price_trigger
    AFTER INSERT ON Rooms
    FOR EACH ROW
    BEGIN
        UPDATE Rooms
        SET price = NEW.capacity * 50 + 500 * NEW.projector + 100 * NEW.mics + 100 * NEW.whiteboard
        WHERE room_id = NEW.room_id;
    END;
    """)

    # Commit changes and close the cursor and connection
    connection.commit()

    print("Tables created successfully.")

except Error as err:
    print(f"Error: {err}")
    connection.rollback()


# Sample data for Users Table
users_data = [
    ('username1', 'admin123', 'admin@example.com', 'Admin', 'admin'),
    ('username2', 'userpass', 'user1@example.com', 'User 1', 'regular'),
    ('username3', 'userpass', 'user2@example.com', 'User 2', 'regular'),
    ('username4', 'ownerpass', 'owner1@example.com', 'Owner 1', 'room owner'),
    ('username5', 'securepass', 'user3@example.com', 'Sara Johnson', 'regular'),
    ('username6', 'pass1234', 'user4@example.com', 'Emily Davis', 'regular'),
    ('username7', 'adminpass', 'admin2@example.com', 'Chris', 'admin'),
    ('username8', 'mypassword', 'user5@example.com', 'Michael Brown', 'regular'),
    ('username9', 'pass456', 'user6@example.com', 'Linda White', 'regular'),
    ('username10', 'ownerpass', 'owner2@example.com', 'David', 'room owner'),
    ('username11', 'userpass', 'user7@example.com', 'Emma Turner', 'regular'),
    ('username12', 'newpassword', 'user8@example.com', 'Ryan Parker', 'regular'),
    ('username13', 'adminadmin', 'admin3@example.com', 'Sophia', 'admin'),
    ('username14', 'pass789', 'user9@example.com', 'Tom Johnson', 'regular')
]

# Sample data for Rooms Table
rooms_data = [
    ('Room A', 20, 1, 0, 1, 100, 'Building A',
     'Small meeting room', 'available'),
    ('Room B', 50, 1, 1, 0, 200, 'Building B',
     'Large conference room', 'available'),
    ('Room C', 10, 0, 0, 0, 300, 'Building C',
     'Small breakout room', 'unavailable'),
    ('Room D', 30, 1, 1, 1, 150, 'Building A',
     'Medium meeting room', 'available'),
    ('Room E', 40, 1, 0, 1, 250, 'Building B',
     'Executive boardroom', 'available'),
    ('Room F', 15, 0, 1, 0, 180, 'Building C',
     'Collaboration space', 'unavailable'),
    ('Room G', 25, 1, 1, 1, 120, 'Building D',
     'Training room', 'available'),
    ('Room H', 60, 1, 0, 0, 300, 'Building E',
     'Auditorium', 'unavailable'),
    ('Room I', 35, 0, 1, 1, 200, 'Building F',
     'Innovation lab', 'available'),
    ('Room J', 45, 1, 1, 0, 250, 'Building G',
     'Presentation room', 'available'),
    ('Room K', 20, 0, 0, 1, 120, 'Building H',
     'Casual meeting space', 'available'),
    ('Room L', 55, 1, 1, 1, 280, 'Building I',
     'Boardroom', 'available'),
    ('Room M', 18, 0, 1, 0, 160, 'Building J',
     'Discussion room', 'unavailable'),
    ('Room N', 50, 1, 1, 1, 220, 'Building K',
     'Collaborative workspace', 'available'),
    ('Room O', 22, 1, 0, 1, 130, 'Building L',
     'Small conference room', 'available'),
    ('Room P', 38, 0, 1, 0, 190, 'Building M',
     'Team huddle room', 'unavailable'),
    ('Room Q', 28, 1, 1, 1, 140, 'Building N',
     'Virtual meeting room', 'available'),
    ('Room R', 42, 0, 0, 1, 170, 'Building O',
     'Breakout session room', 'available'),
    ('Room S', 32, 1, 1, 0, 210, 'Building P',
     'Interactive workshop space', 'available'),
    ('Room T', 48, 0, 1, 1, 240, 'Building Q',
     'Creative studio', 'available'),
    ('Room U', 25, 1, 0, 1, 110, 'Building R',
     'Podcast recording room', 'available'),
    ('Room V', 70, 1, 1, 1, 320, 'Building S',
     'Multipurpose event hall', 'available'),
    ('Room W', 15, 0, 0, 0, 170, 'Building T',
     'Quiet workspace', 'unavailable')
]

# Sample data for Booked Room Table
booked_rooms_data = [
    (2, 1, '2023-11-15 10:00:00',
     '2023-11-15 12:00:00', 'Team Meeting', 'confirmed'),
    (3, 2, '2023-11-16 14:00:00',
     '2023-11-16 16:00:00', 'Presentation', 'confirmed'),
    (2, 3, '2023-11-17 09:00:00', '2023-11-17 10:00:00', 'Interview', 'pending'),
    (4, 1, '2023-11-18 13:30:00',
     '2023-11-18 15:30:00', 'Workshop', 'confirmed'),
    (5, 4, '2023-11-19 11:00:00',
     '2023-11-19 13:00:00', 'Training Session', 'pending'),
    (3, 5, '2023-11-20 15:30:00', '2023-11-20 16:30:00', 'Client Meeting', 'confirmed'),
    (1, 6, '2023-11-21 08:45:00', '2023-11-21 10:15:00', 'Seminar', 'confirmed'),
    (4, 7, '2023-11-22 12:00:00', '2023-11-22 14:00:00', 'Product Launch', 'confirmed')
]
# Sample data for Waiting List Table
waiting_list_data = [
    (4, 3, '2023-11-18 11:00:00', 'pending'),
    (3, 1, '2023-11-19 15:00:00', 'approved'),
    (2, 2, '2023-11-20 08:00:00', 'declined')
]

# Sample data for Notifications Table
notifications_data = [
    (2, 'Your booking is approved. Room A on 2023-11-19',
     '2023-11-18 09:00:00', 'unread'),
    (3, 'New booking request for Room C on 2023-11-20',
     '2023-11-19 14:00:00', 'unread'),
    (1, 'Payment for Room B is due on 2023-11-21', '2023-11-20 16:00:00', 'unread')
]

try:
    # Insert sample data into Users Table
    cursor.executemany(
        "INSERT INTO Users (username, password, email, full_name, user_type) VALUES (?, ?, ?, ?, ?)", users_data)

    # Insert sample data into Rooms Table
    cursor.executemany(
        "INSERT INTO Rooms (room_name, capacity, projector, mics, whiteboard, price, location, description, availability) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", rooms_data)

    # Insert sample data into Booked Room Table
    cursor.executemany(
        "INSERT INTO BookedRoom (user_id, room_id, start_datetime, end_datetime, purpose, status) VALUES (?, ?, ?, ?, ?, ?)", booked_rooms_data)

    # Insert sample data into Waiting List Table
    cursor.executemany(
        "INSERT INTO WaitingList (user_id, room_id, requested_datetime, status) VALUES (?, ?, ?, ?)", waiting_list_data)

    # Insert sample data into Notifications Table
    cursor.executemany(
        "INSERT INTO Notifications (user_id, message, timestamp, status) VALUES (?, ?, ?, ?)", notifications_data)

    # Commit changes and close the cursor and connection
    connection.commit()
    cursor.close()
    connection.close()

    print("Sample data inserted successfully.")

except Error as err:
    print(f"Error: {err}")
    connection.rollback()

# Close the connection
connection.close()
