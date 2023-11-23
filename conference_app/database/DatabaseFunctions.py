import sqlite3
import streamlit as st

import json
import pandas as pd

import pprint

# Database configuration
db_file = "conference_app/database/database.db"

# Function to create a connection to SQLite database


def connect_to_database():
    try:
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
        return connection, cursor
    except sqlite3.Error as err:
        print(f"Database connection error: {err}")
        return None, None

# Function to close the database connection


def close_connection(connection, cursor):
    if connection:
        cursor.close()
        connection.close()

# Function to view rooms


def authenticate(username, password):

    try:
        connection, cursor = connect_to_database()
        if connection:
            cursor.execute(
                "SELECT * FROM Users WHERE username = ? and password = ?", (username, password,))
            user = cursor.fetchone()
            if user:
                print(user)
                return user
            else:
                return None
        close_connection(connection, cursor)
    except Exception as e:
        print(f"Error logging in: {e}")
        return None


def view_rooms():
    try:
        connection, cursor = connect_to_database()
        if connection:

            cursor.execute(
                "SELECT room_id, room_name, capacity, projector, mics, whiteboard, price, location, description, availability FROM Rooms")
            rooms = cursor.fetchall()
            # df = pd.DataFrame(
            #     rooms, columns=["room_id", "room_name", "capacity", "projector", "mics", "whiteboard", "price", "location", "description", "availability"])
            # json_data = df.to_json(orient="records")
            close_connection(connection, cursor)
            print(rooms)
            return rooms
    except Exception as e:
        print(f"Error viewing rooms: {e}")


def view_room_specification(room_id):
    try:
        connection, cursor = connect_to_database()
        if connection:
            cursor.execute(
                "SELECT room_id, room_name, capacity, projector, mics, whiteboard, price, location, description, availability FROM Rooms WHERE room_id = ?", (room_id,))
            room = cursor.fetchone()
            # df = pd.DataFrame(
            #     room, columns=["room_id", "room_name", "capacity", "projector", "mics", "whiteboard", "price", "location", "description", "availability"])

            if room:
                print(room)
            else:
                print("Room not found.")
        close_connection(connection, cursor)
        #
        return room
    except Exception as e:
        print(f"Error viewing room specification: {e}")

# Function to add user


def add_user(username, password, email, full_name, user_type):
    try:
        connection, cursor = connect_to_database()
        if connection:
            cursor.execute("INSERT INTO Users (username, password, email, full_name, user_type) VALUES (?, ?, ?, ?, ?)",
                           (username, password, email, full_name, user_type))
            connection.commit()
            print("User added successfully.")
        close_connection(connection, cursor)
    except Exception as e:
        print(f"Error adding user: {e}")


def add_room(room_name, capacity=100, projector=1, mics=1, whiteboard=1, price=1000, location='', description='', availability='available'):
    try:
        connection, cursor = connect_to_database()
        if connection:
            cursor.execute("INSERT INTO Rooms (room_name, capacity, projector, mics, whiteboard, price, location, description, availability) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                           (room_name, capacity, projector, mics, whiteboard, price, location, description, availability))
            connection.commit()
            print("Room added successfully.")
        close_connection(connection, cursor)
    except Exception as e:
        print(f"Error adding room: {e}")


def update_room(room_id, room_name, capacity, projector, mics, whiteboard, price, location, description, availability):
    try:
        connection, cursor = connect_to_database()
        if connection:
            cursor.execute("UPDATE Rooms SET room_name=?, capacity=?, projector=?, mics=?, whiteboard=?, price=?, location=?, description=?, availability=? WHERE room_id=?",
                           (room_name, capacity, projector, mics, whiteboard, price, location, description, availability, room_id))
            connection.commit()
            print("Room updated successfully.")
        close_connection(connection, cursor)
    except Exception as e:
        print(f"Error updating room: {e}")


def update_room_infra(room_id, capacity, projector, mics, whiteboard):
    try:
        connection, cursor = connect_to_database()
        if connection:
            cursor.execute("UPDATE Rooms SET room_name=?, capacity=?, projector=?, mics=?, whiteboard=?, price=?, location=?, description=?, availability=? WHERE room_id=?",
                           (capacity, projector, mics, whiteboard, room_id))
            connection.commit()
            print("Room updated successfully.")
        close_connection(connection, cursor)
    except Exception as e:
        print(f"Error updating room: {e}")
# Function to remove room


def remove_room(room_id):
    try:
        connection, cursor = connect_to_database()
        if connection:
            cursor.execute("DELETE FROM Rooms WHERE room_id = ?", (room_id,))
            connection.commit()
            print("Room removed successfully.")
        close_connection(connection, cursor)
    except Exception as e:
        print(f"Error removing room: {e}")

# Function to remove user


def remove_user(user_id):
    try:
        connection, cursor = connect_to_database()
        if connection:
            cursor.execute("DELETE FROM Users WHERE user_id = ?", (user_id,))
            connection.commit()
            print("User removed successfully.")
        close_connection(connection, cursor)
    except Exception as e:
        print(f"Error removing user: {e}")

# Function to identify user type


def identify_user_type(username):
    try:
        connection, cursor = connect_to_database()
        if connection:
            cursor.execute(
                "SELECT user_type FROM Users WHERE username = ?", (username,))
            user_type = cursor.fetchone()
            if user_type:
                print(user_type)
                return user_type[0]
            else:
                return None
        close_connection(connection, cursor)
    except Exception as e:
        print(f"Error identifying user type: {e}")
        return None

# Function to join waiting list


def join_waiting_list(user_id, room_id, requested_datetime):
    try:
        connection, cursor = connect_to_database()
        if connection:
            cursor.execute("INSERT INTO WaitingList (user_id, room_id, requested_datetime, status) VALUES (?, ?, ?, 'pending')",
                           (user_id, room_id, requested_datetime))
            connection.commit()
            print("Joined waiting list successfully.")
        close_connection(connection, cursor)
    except Exception as e:
        print(f"Error joining waiting list: {e}")

# Function to show waiting list


def show_waiting_list(room_id):
    try:
        connection, cursor = connect_to_database()
        if connection:
            cursor.execute(
                "SELECT user_id,room_id, requested_datetime,status FROM WaitingList WHERE room_id = ?", (room_id,))
            waiting_list = cursor.fetchall()
            if waiting_list:
                print("Waiting List:")
                for entry in waiting_list:
                    print(entry)
            else:
                print("Waiting list is empty for this room.")
        close_connection(connection, cursor)
        return waiting_list
    except Exception as e:
        print(f"Error showing waiting list: {e}")


def show_waiting_list_for_user(user_id):
    try:
        connection, cursor = connect_to_database()
        if connection:
            cursor.execute(
                "SELECT user_id,room_id, requested_datetime,status FROM WaitingList WHERE user_id = ? and status = 'pending'", (user_id,))
            waiting_list = cursor.fetchall()
            if waiting_list:
                print("Waiting List:")
                for entry in waiting_list:
                    print(entry)
            else:
                print("Waiting list is empty for this room.")
        close_connection(connection, cursor)
        return waiting_list
    except Exception as e:
        print(f"Error showing waiting list: {e}")

# Function to unjoin waiting list


def unjoin_waiting_list(user_id, room_id):
    try:
        connection, cursor = connect_to_database()
        if connection:
            cursor.execute(
                "DELETE FROM WaitingList WHERE user_id = ? AND room_id = ? AND status = 'pending'", (user_id, room_id))
            connection.commit()
            print("Removed from waiting list successfully.")
        close_connection(connection, cursor)
    except Exception as e:
        print(f"Error removing from waiting list: {e}")


def book_room(user_id, room_id_to_book, date_to_book, start_time_to_book, end_time_to_book):
    try:
        connection, cursor = connect_to_database()
        if connection:
            # Insert a new record into the BookedRoom table with status set to 'pending'
            cursor.execute("""
                INSERT INTO BookedRoom (user_id, room_id, start_datetime, end_datetime, status)
                VALUES (?, ?, ?, ?, 'pending')
            """, (user_id, room_id_to_book, f"{date_to_book} {start_time_to_book}", f"{date_to_book} {end_time_to_book}"))

            connection.commit()
            print(f"Room ID {room_id_to_book} booked successfully on {
                  date_to_book} from {start_time_to_book} to {end_time_to_book}.")

    except Exception as e:
        print(f"Error booking room: {e}")
        connection.rollback()

    finally:
        close_connection(connection, cursor)


def get_waiting_list_users(room_id, selected_date):
    try:
        connection, cursor = connect_to_database()
        if connection:
            cursor.execute("""
                SELECT Users.user_id, Users.username
                FROM WaitingList
                INNER JOIN Users ON WaitingList.user_id = Users.user_id
                WHERE WaitingList.room_id = ? AND DATE(WaitingList.requested_datetime) = ?
            """, (room_id, selected_date))

            waiting_list_users = cursor.fetchall()
            return waiting_list_users

    except Exception as e:
        print(f"Error getting waiting list users: {e}")
        return None

# Updated unbook_room function with notification logic


def unbook_room(booking_id):
    try:
        connection, cursor = connect_to_database()
        if connection:
            # Get room_id and date for the canceled booking
            cursor.execute(
                "SELECT room_id, start_datetime FROM BookedRoom WHERE booking_id = ?", (booking_id,))
            canceled_booking = cursor.fetchone()

            if canceled_booking:
                room_id, canceled_date = canceled_booking

                # Update the status of the booking to 'canceled'
                cursor.execute("""
                    UPDATE BookedRoom
                    SET status = 'canceled'
                    WHERE booking_id = ?
                """, (booking_id,))

                # Get users in the waiting list for the room and date
                waiting_list_users = get_waiting_list_users(
                    room_id, canceled_date)

                if waiting_list_users:
                    # Add notifications for users in the waiting list
                    for user in waiting_list_users:
                        cursor.execute("""
                            INSERT INTO Notifications (user_id, message, timestamp, status)
                            VALUES (?, ?, DATETIME('now'), 'unread')
                        """, (user[0], f"The room (ID: {room_id}) is now available on {canceled_date}.",))

                connection.commit()
                print(f"Booking ID {
                      booking_id} canceled successfully. Notifications sent to waiting list users.")

    except Exception as e:
        print(f"Error canceling booking: {e}")
        connection.rollback()

    finally:
        close_connection(connection, cursor)


def view_notifications(user_id):
    try:
        connection, cursor = connect_to_database()
        if connection:
            cursor.execute(
                "SELECT * FROM Notifications WHERE user_id = ?", (user_id,))
            notifications = cursor.fetchall()
            if notifications:
                return notifications
            else:
                print("No notifications found for the given user.")
                return None
        close_connection(connection, cursor)
    except Exception as e:
        print(f"Error retrieving notifications: {e}")
        return None


def view_booked_rooms_for_date(selected_date):
    try:
        connection, cursor = connect_to_database()
        if connection:
            cursor.execute("""
                SELECT BookedRoom.booking_id, Users.username,Rooms.room_id, Rooms.room_name, BookedRoom.start_datetime, BookedRoom.end_datetime, BookedRoom.purpose, BookedRoom.status
                FROM BookedRoom
                INNER JOIN Users ON BookedRoom.user_id = Users.user_id
                INNER JOIN Rooms ON BookedRoom.room_id = Rooms.room_id
                WHERE DATE(BookedRoom.start_datetime) = ? and status ='pending'
            """, (selected_date,))

            booked_rooms = cursor.fetchall()

        close_connection(connection, cursor)
        return booked_rooms
    except Exception as e:
        print(f"Error getting booked rooms: {e}")
        return None


def check_room_availability(room_id, selected_date, start_time, end_time):
    try:
        connection, cursor = connect_to_database()
        if connection:
            # Check if the room is booked for the specified date and time range
            # cursor.execute("""
            #     SELECT *
            #     FROM BookedRoom
            #     WHERE room_id = ?
            #     AND DATE(start_datetime) = ?
            #     AND ((TIME(start_datetime) < ? AND TIME(end_datetime) > ?)
            #         OR (TIME(start_datetime) >= ? AND TIME(start_datetime) < ?)
            #         OR (TIME(end_datetime) > ? AND TIME(end_datetime) <= ?))
            # """, (room_id, selected_date, start_time, start_time, start_time, end_time, end_time, end_time))
            cursor.execute("""
                SELECT *
                FROM BookedRoom
                WHERE room_id = ? 
                AND DATE(start_datetime) = ? 
            """, (room_id, selected_date))

            conflicting_bookings = cursor.fetchall()

            close_connection(connection, cursor)

            if conflicting_bookings:
                print(
                    f"Room {room_id} is not available for the selected date and time range.")
                return False
            else:
                print(
                    f"Room {room_id} is available for the selected date and time range.")
                return True

    except Exception as e:
        print(f"Error checking room availability: {e}")
        return False


def view_booked_rooms():
    try:
        connection, cursor = connect_to_database()
        if connection:
            cursor.execute("""
                SELECT BookedRoom.booking_id, Users.username,Rooms.room_id, Rooms.room_name, BookedRoom.start_datetime, BookedRoom.end_datetime, BookedRoom.purpose
                FROM BookedRoom
                INNER JOIN Users ON BookedRoom.user_id = Users.user_id
                INNER JOIN Rooms ON BookedRoom.room_id = Rooms.room_id
            """)

            booked_rooms = cursor.fetchall()

        close_connection(connection, cursor)
        return booked_rooms
    except Exception as e:
        print(f"Error getting booked rooms: {e}")
        return None

#
# TESTING FUNCTIONS:


# print(view_booked_rooms_for_date("2023-11-17"))

# print(identify_user_type("admin"))

# update_room(2, 'Room B', 25, 1, 1, 0, 200,
# 'Building B', 'Large conference room', 'available')


# # join_waiting_list(4, 3)
# join_waiting_list(2, 3, '2023-11-20 08:00:00')
# show_waiting_list(3)

# Sample usage of the functions
# if __name__ == "__main__":
#     st.title("Conference Room Booking System")

#     # Create the "View Rooms" button
#     if st.button("View Rooms"):
#         rooms_text = view_rooms()
#         st.text(rooms_text)

#     # Create the "View Room Specification" button
#     st.header("View Room Specification")
#     room_id = st.number_input("Enter Room ID:")
#     if st.button("View Room Specification"):
#         room_spec_text = view_room_specification(int(room_id))
#         st.text(room_spec_text)

#     # Create the "Add User" button
#     st.header("Add User")
#     username = st.text_input("Username:")
#     password = st.text_input("Password:", type="password")
#     email = st.text_input("Email:")
#     full_name = st.text_input("Full Name:")
#     user_type = st.selectbox("User Type", ["admin", "regular", "room owner"])
#     if st.button("Add User"):
#         add_user(username, password, email, full_name, user_type)

#     # Create the "Add Room" button
#     st.header("Add Room")
#     room_name = st.text_input("Room Name:")
#     capacity = st.number_input("Capacity:")
#     projector = st.number_input("Projector:")
#     mics = st.number_input("Mics:")
#     whiteboard = st.number_input("Whiteboard:")
#     price = st.number_input("Price:")
#     location = st.text_input("Location:")
#     description = st.text_area("Description:")
#     availability = st.selectbox("Availability", ["available", "unavailable"])
#     if st.button("Add Room"):
#         add_room(room_name, capacity, projector, mics, whiteboard,
#                  price, location, description, availability)

#     # Create the "Update Room" button
#     st.header("Update Room")
#     update_room_id = st.number_input("Enter Room ID to Update:")
#     updated_room_name = st.text_input("Updated Room Name:")
#     updated_capacity = st.number_input("Updated Capacity:")
#     updated_projector = st.number_input("Updated Projector:")
#     updated_mics = st.number_input("Updated Mics:")
#     updated_whiteboard = st.number_input("Updated Whiteboard:")
#     updated_price = st.number_input("Updated Price:")
#     updated_location = st.text_input("Updated Location:")
#     updated_description = st.text_area("Updated Description:")
#     updated_availability = st.selectbox(
#         "Updated Availability", ["available", "unavailable"])
#     if st.button("Update Room"):
#         update_room(update_room_id, updated_room_name, updated_capacity, updated_projector, updated_mics,
#                     updated_whiteboard, updated_price, updated_location, updated_description, updated_availability)

#     delete_room_id = st.number_input("Enter Room ID to Delete:")
#     if st.button("Remove Room"):
#         remove_room(delete_room_id)

#     # Create the "Close Connection" button
#     if st.button("Close Connection"):
#         st.text("Connection Closed.")
