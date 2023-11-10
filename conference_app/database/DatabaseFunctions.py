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


def add_room(room_name, capacity, projector, mics, whiteboard, price, location, description, availability):
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
                "SELECT user_id,room_id, requested_datetime,status FROM WaitingList WHERE room_id = ? AND status = 'pending'", (room_id,))
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
                SELECT BookedRoom.booking_id, Users.username, Rooms.room_name, BookedRoom.start_datetime, BookedRoom.end_datetime, BookedRoom.purpose, BookedRoom.status
                FROM BookedRoom
                INNER JOIN Users ON BookedRoom.user_id = Users.user_id
                INNER JOIN Rooms ON BookedRoom.room_id = Rooms.room_id
                WHERE DATE(BookedRoom.start_datetime) = ?
            """, (selected_date,))

            booked_rooms = cursor.fetchall()

        close_connection(connection, cursor)
        return booked_rooms
    except Exception as e:
        print(f"Error getting booked rooms: {e}")
        return None


# TESTING FUNCTIONS:


# print(view_booked_rooms_for_date("2023-11-17"))

# print(view_notifications(2))

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
