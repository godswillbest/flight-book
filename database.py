"""
database.py
===========
Handles all SQLite database operations for the Flight Booking System.
This module uses Python's built-in sqlite3 library to create, read,
update, and delete booking and flight data.
"""

import sqlite3
import os
from datetime import datetime


# ─── Database File Path ────────────────────────────────────────────────────────
DB_PATH = "flight_bookings.db"


# ─── Database Connection Helper ────────────────────────────────────────────────
def get_connection():
    """
    Creates and returns a connection to the SQLite database.
    Using check_same_thread=False allows Streamlit's multi-threaded
    environment to work without errors.
    """
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row  # enables column access by name
    return conn


# ─── Database Initialization ───────────────────────────────────────────────────
def init_db():
    """
    Creates all necessary database tables if they don't already exist.
    Called once when the app starts up.
    Tables:
        - flights: stores all available flight routes
        - bookings: stores confirmed passenger bookings
        - passengers: stores individual passenger details per booking
    """
    conn = get_connection()
    cursor = conn.cursor()

    # ── Flights Table ──────────────────────────────────────────────────────────
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS flights (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            flight_number   TEXT NOT NULL UNIQUE,
            airline         TEXT NOT NULL,
            origin          TEXT NOT NULL,
            destination     TEXT NOT NULL,
            departure_time  TEXT NOT NULL,
            arrival_time    TEXT NOT NULL,
            duration        TEXT NOT NULL,
            economy_price   REAL NOT NULL,
            business_price  REAL NOT NULL,
            first_price     REAL NOT NULL,
            total_seats     INTEGER NOT NULL,
            available_seats INTEGER NOT NULL,
            aircraft        TEXT
        )
    """)

    # ── Bookings Table ─────────────────────────────────────────────────────────
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            booking_ref     TEXT NOT NULL UNIQUE,
            flight_id       INTEGER NOT NULL,
            flight_number   TEXT NOT NULL,
            booking_date    TEXT NOT NULL,
            travel_date     TEXT NOT NULL,
            flight_class    TEXT NOT NULL,
            total_passengers INTEGER NOT NULL,
            total_price     REAL NOT NULL,
            status          TEXT DEFAULT 'Confirmed',
            FOREIGN KEY (flight_id) REFERENCES flights(id)
        )
    """)

    # ── Passengers Table ───────────────────────────────────────────────────────
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS passengers (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            booking_ref     TEXT NOT NULL,
            first_name      TEXT NOT NULL,
            last_name       TEXT NOT NULL,
            passport_number TEXT NOT NULL,
            date_of_birth   TEXT NOT NULL,
            nationality     TEXT NOT NULL,
            seat_number     TEXT NOT NULL,
            FOREIGN KEY (booking_ref) REFERENCES bookings(booking_ref)
        )
    """)

    conn.commit()
    conn.close()


# ─── Flight Seeder ─────────────────────────────────────────────────────────────
def seed_flights():
    """
    Populates the flights table with realistic dummy data if it's empty.
    This gives users flights to search for without needing a real airline API.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Only seed if no flights exist
    cursor.execute("SELECT COUNT(*) FROM flights")
    if cursor.fetchone()[0] > 0:
        conn.close()
        return

    # Realistic flight data covering major African, European, and global routes
    flights = [
        # ── Lagos (LOS) Departures ─────────────────────────────────────────────
        ("LH401",  "Lufthansa",        "Lagos",      "London",      "06:00", "12:30", "6h 30m", 320.00, 950.00,  2200.00, 180, 143, "Airbus A380"),
        ("BA072",  "British Airways",  "Lagos",      "London",      "09:15", "15:55", "6h 40m", 310.00, 920.00,  2100.00, 165, 120, "Boeing 777"),
        ("ET904",  "Ethiopian Air",    "Lagos",      "Dubai",       "11:00", "22:15", "7h 15m", 280.00, 780.00,  1800.00, 200, 167, "Boeing 787"),
        ("QR1439", "Qatar Airways",    "Lagos",      "Doha",        "02:30", "13:00", "6h 30m", 295.00, 850.00,  1950.00, 210, 189, "Airbus A350"),
        ("EK783",  "Emirates",         "Lagos",      "Dubai",       "23:59", "11:35", "7h 36m", 340.00, 980.00,  2400.00, 220, 198, "Airbus A380"),
        ("AF549",  "Air France",       "Lagos",      "Paris",       "13:45", "20:30", "6h 45m", 305.00, 890.00,  2050.00, 175, 140, "Boeing 787"),
        ("TK624",  "Turkish Airlines", "Lagos",      "Istanbul",    "07:30", "17:15", "5h 45m", 270.00, 760.00,  1750.00, 190, 155, "Boeing 737"),
        ("MS839",  "EgyptAir",         "Lagos",      "Cairo",       "08:20", "13:50", "5h 30m", 210.00, 580.00,  1300.00, 160, 134, "Airbus A220"),
        ("AT500",  "Royal Air Maroc",  "Lagos",      "Casablanca",  "10:00", "14:45", "4h 45m", 190.00, 520.00,  1150.00, 150, 112, "Boeing 737"),
        ("W3 101", "Arik Air",         "Lagos",      "Abuja",       "06:30", "07:15", "0h 45m",  55.00, 140.00,   320.00, 100,  78, "Bombardier Q400"),
        ("P4 201", "Air Peace",        "Lagos",      "Accra",       "09:00", "10:10", "1h 10m",  95.00, 230.00,   490.00, 120,  95, "Embraer E190"),
        ("KQ102",  "Kenya Airways",    "Lagos",      "Nairobi",     "15:00", "22:30", "7h 30m", 260.00, 720.00,  1650.00, 180, 152, "Boeing 787"),

        # ── Abuja (ABV) Departures ────────────────────────────────────────────
        ("LH403",  "Lufthansa",        "Abuja",      "Frankfurt",   "07:00", "14:30", "7h 30m", 340.00, 980.00,  2250.00, 175, 143, "Boeing 747"),
        ("BA074",  "British Airways",  "Abuja",      "London",      "10:30", "17:00", "6h 30m", 320.00, 940.00,  2150.00, 165, 121, "Boeing 777"),
        ("W3 103", "Arik Air",         "Abuja",      "Lagos",       "08:00", "08:45", "0h 45m",  55.00, 140.00,   320.00, 100,  82, "Bombardier Q400"),
        ("P4 203", "Air Peace",        "Abuja",      "Port Harcourt","11:00","11:50", "0h 50m",  50.00, 125.00,   290.00,  90,  67, "Embraer E175"),

        # ── London (LHR) Departures ───────────────────────────────────────────
        ("BA073",  "British Airways",  "London",     "Lagos",       "13:00", "19:30", "6h 30m", 290.00, 880.00,  2050.00, 165, 130, "Boeing 777"),
        ("VS401",  "Virgin Atlantic",  "London",     "New York",    "11:30", "14:15", "8h 45m", 410.00, 1200.00, 3500.00, 200, 167, "Airbus A350"),
        ("BA175",  "British Airways",  "London",     "New York",    "09:00", "12:05", "8h 05m", 390.00, 1150.00, 3300.00, 210, 189, "Boeing 787"),
        ("LH902",  "Lufthansa",        "London",     "Frankfurt",   "07:00", "09:30", "2h 30m", 120.00, 350.00,   850.00, 150, 123, "Airbus A320"),

        # ── Dubai (DXB) Departures ────────────────────────────────────────────
        ("EK782",  "Emirates",         "Dubai",      "Lagos",       "03:35", "09:00", "7h 25m", 320.00, 960.00,  2350.00, 220, 191, "Airbus A380"),
        ("EK001",  "Emirates",         "Dubai",      "London",      "08:00", "12:30", "7h 30m", 450.00, 1350.00, 3800.00, 220, 187, "Airbus A380"),
        ("FZ101",  "flydubai",         "Dubai",      "Cairo",       "06:00", "08:30", "2h 30m", 130.00, 380.00,   890.00, 160, 134, "Boeing 737 MAX"),
        ("QR100",  "Qatar Airways",    "Dubai",      "Doha",        "09:00", "10:00", "1h 00m",  90.00, 250.00,   580.00, 130, 107, "Airbus A320"),

        # ── New York (JFK) Departures ─────────────────────────────────────────
        ("AA100",  "American Airlines","New York",   "London",      "22:00", "10:00", "7h 00m", 380.00, 1100.00, 3200.00, 200, 171, "Boeing 777"),
        ("DL401",  "Delta Airlines",   "New York",   "Paris",       "18:30", "08:00", "7h 30m", 395.00, 1150.00, 3350.00, 195, 163, "Airbus A330"),
        ("UA902",  "United Airlines",  "New York",   "Dubai",       "23:00", "19:00", "12h 00m",490.00, 1450.00, 4200.00, 210, 187, "Boeing 777"),

        # ── Nairobi (NBO) Departures ──────────────────────────────────────────
        ("KQ101",  "Kenya Airways",    "Nairobi",    "Lagos",       "08:00", "11:30", "7h 30m", 250.00, 710.00,  1620.00, 180, 149, "Boeing 787"),
        ("ET303",  "Ethiopian Air",    "Nairobi",    "Addis Ababa", "09:00", "11:00", "2h 00m", 110.00, 310.00,   720.00, 155, 128, "Airbus A350"),
        ("KQ003",  "Kenya Airways",    "Nairobi",    "London",      "23:30", "06:30", "9h 00m", 360.00, 1050.00, 2400.00, 180, 155, "Boeing 787"),

        # ── Accra (ACC) Departures ────────────────────────────────────────────
        ("P4 202", "Air Peace",        "Accra",      "Lagos",       "12:00", "13:10", "1h 10m",  95.00, 230.00,   490.00, 120,  98, "Embraer E190"),
        ("ET906",  "Ethiopian Air",    "Accra",      "Addis Ababa", "08:30", "15:00", "6h 30m", 240.00, 680.00,  1560.00, 175, 142, "Boeing 787"),

        # ── Johannesburg (JNB) Departures ─────────────────────────────────────
        ("SA231",  "South African",    "Johannesburg","Lagos",       "09:00", "14:30", "7h 30m", 270.00, 760.00,  1740.00, 185, 154, "Airbus A340"),
        ("SA001",  "South African",    "Johannesburg","London",      "18:00", "05:30", "11h 30m",420.00, 1250.00, 2900.00, 185, 161, "Airbus A340"),
        ("QR1441", "Qatar Airways",    "Johannesburg","Doha",        "22:00", "07:30", "9h 30m", 380.00, 1100.00, 2550.00, 210, 183, "Boeing 777"),
    ]

    # Columns match the flights table definition
    cursor.executemany("""
        INSERT OR IGNORE INTO flights
        (flight_number, airline, origin, destination, departure_time,
         arrival_time, duration, economy_price, business_price, first_price,
         total_seats, available_seats, aircraft)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, flights)

    conn.commit()
    conn.close()


# ─── Flight Queries ────────────────────────────────────────────────────────────
def search_flights(origin: str, destination: str) -> list:
    """
    Returns all flights matching the given origin and destination.
    Case-insensitive search using SQL LOWER().
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM flights
        WHERE LOWER(origin) = LOWER(?)
          AND LOWER(destination) = LOWER(?)
          AND available_seats > 0
        ORDER BY departure_time
    """, (origin.strip(), destination.strip()))
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return results


def get_all_flights() -> list:
    """Returns all flights in the database, for the admin panel."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM flights ORDER BY airline, flight_number")
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return results


def get_available_cities() -> list:
    """
    Returns a sorted, deduplicated list of all cities that appear
    as either an origin or destination in the flights table.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DISTINCT origin AS city FROM flights
        UNION
        SELECT DISTINCT destination AS city FROM flights
        ORDER BY city
    """)
    cities = [row["city"] for row in cursor.fetchall()]
    conn.close()
    return cities


# ─── Booking Operations ────────────────────────────────────────────────────────
def create_booking(booking_data: dict, passengers_data: list) -> bool:
    """
    Saves a new booking and all passenger records to the database.
    Also decrements available_seats on the chosen flight.

    Args:
        booking_data: dict with booking-level info (ref, flight_id, price, etc.)
        passengers_data: list of dicts, one per passenger

    Returns:
        True if successful, False otherwise
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Insert the main booking record
        cursor.execute("""
            INSERT INTO bookings
            (booking_ref, flight_id, flight_number, booking_date,
             travel_date, flight_class, total_passengers, total_price, status)
            VALUES (:booking_ref, :flight_id, :flight_number, :booking_date,
                    :travel_date, :flight_class, :total_passengers, :total_price, :status)
        """, booking_data)

        # Insert each passenger
        for p in passengers_data:
            cursor.execute("""
                INSERT INTO passengers
                (booking_ref, first_name, last_name, passport_number,
                 date_of_birth, nationality, seat_number)
                VALUES (:booking_ref, :first_name, :last_name, :passport_number,
                        :date_of_birth, :nationality, :seat_number)
            """, p)

        # Reduce available seats on the flight
        cursor.execute("""
            UPDATE flights
            SET available_seats = available_seats - ?
            WHERE id = ?
        """, (booking_data["total_passengers"], booking_data["flight_id"]))

        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"[DB ERROR] create_booking: {e}")
        return False
    finally:
        conn.close()


def get_booking(booking_ref: str) -> dict | None:
    """Fetches a single booking by its reference code."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bookings WHERE booking_ref = ?", (booking_ref,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def get_booking_passengers(booking_ref: str) -> list:
    """Returns all passengers associated with a booking reference."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM passengers WHERE booking_ref = ?", (booking_ref,))
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return results


def get_all_bookings() -> list:
    """Returns every booking record (for admin view), newest first."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bookings ORDER BY booking_date DESC")
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return results


def cancel_booking(booking_ref: str) -> bool:
    """
    Marks a booking as 'Cancelled' and restores the seat count on the flight.
    Returns True on success.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Get booking info to know how many seats to restore
        cursor.execute("SELECT * FROM bookings WHERE booking_ref = ?", (booking_ref,))
        booking = cursor.fetchone()
        if not booking or booking["status"] == "Cancelled":
            return False

        # Update status
        cursor.execute("""
            UPDATE bookings SET status = 'Cancelled' WHERE booking_ref = ?
        """, (booking_ref,))

        # Restore seats
        cursor.execute("""
            UPDATE flights
            SET available_seats = available_seats + ?
            WHERE id = ?
        """, (booking["total_passengers"], booking["flight_id"]))

        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"[DB ERROR] cancel_booking: {e}")
        return False
    finally:
        conn.close()


# ─── Admin / Statistics Queries ────────────────────────────────────────────────
def get_statistics() -> dict:
    """
    Aggregates key metrics for the admin dashboard.
    Returns a dict with total_bookings, confirmed, cancelled,
    total_revenue, and most_popular_route.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM bookings")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM bookings WHERE status = 'Confirmed'")
    confirmed = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM bookings WHERE status = 'Cancelled'")
    cancelled = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(total_price) FROM bookings WHERE status = 'Confirmed'")
    revenue_row = cursor.fetchone()[0]
    revenue = revenue_row if revenue_row else 0.0

    cursor.execute("""
        SELECT f.origin, f.destination, COUNT(b.id) AS cnt
        FROM bookings b
        JOIN flights f ON b.flight_id = f.id
        WHERE b.status = 'Confirmed'
        GROUP BY f.origin, f.destination
        ORDER BY cnt DESC
        LIMIT 1
    """)
    pop = cursor.fetchone()
    popular = f"{pop['origin']} → {pop['destination']}" if pop else "N/A"

    conn.close()
    return {
        "total_bookings": total,
        "confirmed": confirmed,
        "cancelled": cancelled,
        "total_revenue": revenue,
        "popular_route": popular,
    }
