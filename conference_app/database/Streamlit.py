import streamlit as st
from DatabaseFunctions import *
import pandas as pd
# Set page configuration
st.set_page_config(layout="wide")

# Initialize session state variables
if 'user' not in st.session_state:
    st.session_state.user = ""
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'page' not in st.session_state:
    st.session_state.page = "Login"

# Function to handle the login page


def set_page(page):
    st.session_state.page = page


def login_page():
    st.title("Conference App Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login!")

    if login_button:
        user = authenticate(username, password)
        if user:
            st.session_state.user = user
            st.session_state.logged_in = True
            st.success(f"Logged in as {user[1]} ({user[5]})")
            set_page("home")
            st.rerun()

# Function to handle ViewRooms option


def view_rooms_for_date_option():
    st.title("View Rooms")

    selected_date = st.date_input(
        "Select a date to see available rooms:", key="date_input")

    if selected_date:
        # Display available rooms for the selected date
        booked_rooms = view_booked_rooms_for_date(selected_date)

        # Extract room IDs from booked rooms
        booked_room_ids = [room[2] for room in booked_rooms]
        all_rooms = view_rooms()

        # Display available rooms (all rooms - booked rooms)
        available_rooms = [
            room for room in all_rooms if room[0] not in booked_room_ids]

        st.header(f"Available Rooms on {selected_date}")
        if available_rooms:

            df_rooms = pd.DataFrame(available_rooms, columns=["Room ID", "Room Name", "Capacity", "Projector",
                                    "Mics", "Whiteboard", "Price", "Location", "Description", "Availability"])
            st.table(df_rooms)
        else:
            st.warning(f"No available rooms on {selected_date}.")
# Function to handle BookRooms option


def view_rooms_option():
    st.title("View Rooms")

    if False:
        pass
    else:
        # Display all rooms
        rooms = view_rooms()
        df_rooms = pd.DataFrame(rooms, columns=["Room ID", "Room Name", "Capacity", "Projector",
                                "Mics", "Whiteboard", "Price", "Location", "Description", "Availability"])

        if rooms:
            st.table(df_rooms)

            # st.header("All Rooms")
            # for room in rooms:
            #     st.write(room)


def book_rooms_option():
    st.title("Book Rooms")
    # book_rooms()

# Function to handle WaitingList option


def waiting_list_option(user_id):
    st.title("Waiting List")

    # Option to join waiting list
    st.header("Join Waiting List")
    st.header("current userID :" + str(user_id))
    room_id_to_join = st.text_input("Enter Room ID to join waiting list:")
    requested_datetime = st.date_input("Select Date to join waiting list:")
    join_waiting_list_button = st.button("Join Waiting List")

    if join_waiting_list_button and room_id_to_join and requested_datetime:
        join_waiting_list(user_id, room_id_to_join, requested_datetime)
        st.success(f"Successfully joined waiting list for Room ID {
                   room_id_to_join} on {requested_datetime}.")

    # Current waiting lists user is part of
    st.header("Current Waiting Lists")
    current_waiting_lists = show_waiting_list_for_user(user_id)
    if current_waiting_lists:

        df_rooms = pd.DataFrame(current_waiting_lists, columns=[
                                "User ID", "Room ID", "Requested Date and Time", "Status"])
        st.table(df_rooms)
    else:
        st.warning("You are not part of any waiting lists.")

    # Option to unjoin waiting list
    st.header("Unjoin Waiting List")
    room_id_to_unjoin = st.text_input("Enter Room ID to unjoin waiting list:")
    unjoin_waiting_list_button = st.button("Unjoin Waiting List")

    if unjoin_waiting_list_button and room_id_to_unjoin:
        unjoin_waiting_list(user_id, room_id_to_unjoin)
        st.rerun()
        st.success(f"Successfully unjoined waiting list for Room ID {
                   room_id_to_unjoin}.")

    room_id_to_show_waiting_list = st.text_input(
        "Enter Room ID to show waiting list:")
    show_waiting_list_button = st.button("Show Waiting List")

    if show_waiting_list_button and room_id_to_show_waiting_list:
        waiting_list_for_room = show_waiting_list(room_id_to_show_waiting_list)
        if waiting_list_for_room:

            df_rooms = pd.DataFrame(waiting_list_for_room, columns=[
                                    "User ID", "Room ID", "Requested Date and Time", "status"])
            st.table(df_rooms)
        else:
            st.warning("No waiting list entries for the specified room.")

    # Display all booked rooms with their date and time
    st.header("All Booked Rooms")
    booked_rooms = view_booked_rooms()
    if booked_rooms:

        df_rooms = pd.DataFrame(booked_rooms, columns=[
                                "booking_id", "username", "room_id", "room_name", "start_time", "end_time", "Purpose"])

        st.table(df_rooms)
    else:
        st.warning("No rooms are booked.")
# Function to handle Notification option


def notifications_option():
    st.title("Notifications")
    # notifications()

# Function to handle ManageUserProfile option


def manage_user_profile_option():
    st.title("Manage User Profile")
    # manage_user_profile()

# Function to handle AdminAccess option


def admin_access_option():
    st.title("Admin Access")
    # admin_access()


# Sidebar with buttons for navigation
st.sidebar.title("Navigation")

if not st.session_state.logged_in:
    st.sidebar.button("Login", on_click=set_page, args=("Login",))
else:

    if st.session_state.page == "home":
        st.title("Welcome to Conference Room Booking System")
    st.sidebar.button("View Rooms", on_click=set_page, args=("ViewRooms",))
    st.sidebar.button("View Rooms By Date", on_click=set_page,
                      args=("ViewRoomsForDate",))
    st.sidebar.button("Book Rooms", on_click=set_page, args=("BookRooms",))
    st.sidebar.button("Waiting List", on_click=set_page, args=("WaitingList",))
    st.sidebar.button("Notifications", on_click=set_page,
                      args=("Notification",))
    st.sidebar.button("Manage User Profile", on_click=set_page,
                      args=("ManageUserProfile",))
    st.sidebar.button("Admin Access", on_click=set_page, args=("AdminAccess",))

# Display content based on selected page
if st.session_state.page == "Login":
    login_page()
elif st.session_state.page == "ViewRooms":
    view_rooms_option()
elif st.session_state.page == "ViewRoomsForDate":
    view_rooms_for_date_option()
elif st.session_state.page == "BookRooms":
    book_rooms_option()
elif st.session_state.page == "WaitingList":
    waiting_list_option(st.session_state.user[0])
elif st.session_state.page == "Notification":
    notifications_option()
elif st.session_state.page == "ManageUserProfile":
    manage_user_profile_option()
elif st.session_state.page == "AdminAccess":
    admin_access_option()
