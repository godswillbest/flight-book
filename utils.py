"""
utils.py
========
Utility / helper functions used across the Flight Booking System.
Includes reference generation, seat mapping, ticket rendering,
price calculation, and input validation helpers.
"""

import random
import string
from datetime import datetime, date


# ─── Booking Reference Generator ──────────────────────────────────────────────
def generate_booking_ref() -> str:
    """
    Creates a unique 8-character booking reference like 'SKY-A3F9-X2'.
    Format: SKY-XXXX-XX (letters + digits, uppercase)
    """
    chars = string.ascii_uppercase + string.digits
    part1 = "".join(random.choices(chars, k=4))
    part2 = "".join(random.choices(chars, k=2))
    return f"SKY-{part1}-{part2}"


# ─── Seat Map Generator ────────────────────────────────────────────────────────
def generate_seat_map(flight_class: str, total_seats: int = 30) -> list[str]:
    """
    Generates a list of available seat numbers for the given class.
    Seat numbering convention:
        First Class:  1A–4F  (rows 1–4,  6 seats per row)
        Business:     5A–10F (rows 5–10, 6 seats per row)
        Economy:      11A–30F (rows 11–30, 6 seats per row)

    Returns a shuffled list to simulate some seats already taken.
    """
    columns = ["A", "B", "C", "D", "E", "F"]

    if flight_class == "First Class":
        rows = range(1, 5)        # rows 1–4
    elif flight_class == "Business":
        rows = range(5, 11)       # rows 5–10
    else:                         # Economy
        rows = range(11, 31)      # rows 11–30

    all_seats = [f"{r}{c}" for r in rows for c in columns]

    # Randomly remove some seats to simulate occupied ones (50–80% available)
    available_count = int(len(all_seats) * random.uniform(0.5, 0.85))
    available_seats = random.sample(all_seats, available_count)
    return sorted(available_seats, key=lambda s: (int(s[:-1]), s[-1]))


# ─── Price Calculator ──────────────────────────────────────────────────────────
def calculate_total_price(base_price: float, passengers: int,
                          travel_date: date) -> float:
    """
    Calculates the final ticket price with a small surge multiplier
    applied when the travel date is within 7 days (last-minute bookings).

    Args:
        base_price:   price per passenger for the selected class
        passengers:   number of passengers
        travel_date:  the date of travel (datetime.date)

    Returns:
        Total price rounded to 2 decimal places.
    """
    days_until_travel = (travel_date - date.today()).days
    surge = 1.25 if days_until_travel <= 7 else 1.0
    return round(base_price * passengers * surge, 2)


# ─── Duration Parser ───────────────────────────────────────────────────────────
def parse_duration_minutes(duration_str: str) -> int:
    """
    Converts a duration string like '6h 30m' into total minutes (390).
    Falls back to 0 if the format is unexpected.
    """
    try:
        parts = duration_str.lower().replace("h", "").replace("m", "").split()
        hours = int(parts[0]) if len(parts) > 0 else 0
        mins = int(parts[1]) if len(parts) > 1 else 0
        return hours * 60 + mins
    except Exception:
        return 0


# ─── Input Validators ─────────────────────────────────────────────────────────
def validate_passenger_data(passenger: dict) -> tuple[bool, str]:
    """
    Validates a single passenger's input dictionary.
    Returns (True, "") if valid, or (False, error_message) if not.
    """
    required = ["first_name", "last_name", "passport_number",
                "date_of_birth", "nationality", "seat_number"]

    for field in required:
        if not passenger.get(field, "").strip():
            return False, f"'{field.replace('_', ' ').title()}' is required."

    # Passport must be at least 5 characters
    if len(passenger["passport_number"].strip()) < 5:
        return False, "Passport number must be at least 5 characters."

    # Date of birth sanity check
    try:
        dob = datetime.strptime(passenger["date_of_birth"], "%Y-%m-%d").date()
        if dob >= date.today():
            return False, "Date of birth must be in the past."
        age = (date.today() - dob).days // 365
        if age > 120:
            return False, "Please enter a valid date of birth."
    except ValueError:
        return False, "Date of birth format is invalid."

    return True, ""


# ─── Ticket Text Generator ─────────────────────────────────────────────────────
def generate_ticket_text(booking: dict, passengers: list, flight: dict) -> str:
    """
    Produces a plain-text boarding-pass style ticket string
    that can be displayed or downloaded.

    Args:
        booking:    dict from the bookings table
        passengers: list of dicts from the passengers table
        flight:     dict from the flights table

    Returns:
        Formatted string representing the ticket.
    """
    divider = "═" * 52
    thin = "─" * 52

    lines = [
        divider,
        "  ✈  SKYLINE AIRWAYS — ELECTRONIC TICKET",
        divider,
        f"  Booking Ref  :  {booking['booking_ref']}",
        f"  Status       :  {booking['status']}",
        f"  Booked On    :  {booking['booking_date']}",
        thin,
        f"  Flight       :  {booking['flight_number']}  ({flight.get('airline', '')})",
        f"  Route        :  {flight.get('origin', '')}  →  {flight.get('destination', '')}",
        f"  Date         :  {booking['travel_date']}",
        f"  Departs      :  {flight.get('departure_time', '')}",
        f"  Arrives      :  {flight.get('arrival_time', '')}",
        f"  Duration     :  {flight.get('duration', '')}",
        f"  Aircraft     :  {flight.get('aircraft', 'N/A')}",
        f"  Class        :  {booking['flight_class']}",
        thin,
    ]

    for i, p in enumerate(passengers, 1):
        lines.append(f"  PASSENGER {i}")
        lines.append(f"    Name         :  {p['first_name']} {p['last_name']}")
        lines.append(f"    Passport     :  {p['passport_number']}")
        lines.append(f"    Nationality  :  {p['nationality']}")
        lines.append(f"    Seat         :  {p['seat_number']}")
        if i < len(passengers):
            lines.append("    " + "· " * 24)

    lines += [
        thin,
        f"  TOTAL PAID   :  ${booking['total_price']:,.2f} USD",
        divider,
        "  Thank you for flying with Skyline Airways!",
        "  Have a safe and pleasant journey.",
        divider,
    ]

    return "\n".join(lines)


# ─── Formatting Helpers ────────────────────────────────────────────────────────
def format_price(amount: float, currency: str = "USD") -> str:
    """Formats a float as a currency string, e.g. $1,234.00 USD"""
    return f"${amount:,.2f} {currency}"


def get_class_emoji(flight_class: str) -> str:
    """Returns a fitting emoji for each flight class."""
    mapping = {
        "Economy":     "🪑",
        "Business":    "💼",
        "First Class": "👑",
    }
    return mapping.get(flight_class, "✈️")


def get_airline_logo_emoji(airline: str) -> str:
    """Maps airline names to a representative emoji for display."""
    mapping = {
        "Emirates":        "🇦🇪",
        "British Airways": "🇬🇧",
        "Lufthansa":       "🇩🇪",
        "Air France":      "🇫🇷",
        "Turkish Airlines":"🇹🇷",
        "Qatar Airways":   "🇶🇦",
        "Ethiopian Air":   "🇪🇹",
        "Kenya Airways":   "🇰🇪",
        "EgyptAir":        "🇪🇬",
        "Arik Air":        "🇳🇬",
        "Air Peace":       "🇳🇬",
        "Royal Air Maroc": "🇲🇦",
        "South African":   "🇿🇦",
        "American Airlines":"🇺🇸",
        "Delta Airlines":  "🇺🇸",
        "United Airlines": "🇺🇸",
        "Virgin Atlantic": "🇬🇧",
        "flydubai":        "🇦🇪",
    }
    for key in mapping:
        if key.lower() in airline.lower():
            return mapping[key]
    return "✈️"
