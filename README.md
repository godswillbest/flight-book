# ✈️ Skyline Airways — Flight Booking System

A complete, production-quality **Flight Booking Ticket System** built with Python and Streamlit.
Designed to be beginner-friendly while meeting university project standards.

---

## 📁 Project Structure

```
flight_booking_system/
│
├── app.py           ← Main Streamlit application (UI + page routing)
├── database.py      ← All SQLite database operations (OOP-ready helpers)
├── utils.py         ← Helper functions: pricing, seat maps, ticket gen, validation
├── requirements.txt ← Python dependencies
└── README.md        ← This file
```

> **Note:** `flight_bookings.db` is auto-created in the same folder when you first run the app.

---

## 🚀 Quick Start

### 1 — Prerequisites
Make sure you have **Python 3.10+** installed.

```bash
python --version   # should print Python 3.10.x or higher
```

### 2 — Clone / Download
Download the project folder, then open a terminal inside it.

### 3 — Create a Virtual Environment (recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 4 — Install Dependencies
```bash
pip install -r requirements.txt
```

### 5 — Run the App
```bash
streamlit run app.py
```

The browser should open automatically at `http://localhost:8501`.

---

## 🗺️ Pages & Features

| Page | Description |
|------|-------------|
| 🏠 **Home** | Hero banner, popular routes, statistics, and airline highlights |
| 🔍 **Search Flights** | Search by city, date, passengers & class → view flight cards → book |
| 📋 **My Booking** | Look up any booking by reference number, view passengers, download ticket |
| 🛡️ **Admin Panel** | PIN-protected dashboard with stats, all bookings table, flight list, and cancel feature |

### Admin PIN
The demo admin PIN is **`1234`**.
Change it in `app.py` in the `page_admin()` function.

---

## ✈️ Sample Flight Routes

The system is pre-loaded with **35+ realistic flights** covering:

- 🇳🇬 Nigeria (Lagos, Abuja, Port Harcourt)
- 🇬🇧 United Kingdom (London)
- 🇩🇪 Germany (Frankfurt)
- 🇫🇷 France (Paris)
- 🇦🇪 UAE (Dubai)
- 🇶🇦 Qatar (Doha)
- 🇹🇷 Turkey (Istanbul)
- 🇪🇬 Egypt (Cairo)
- 🇲🇦 Morocco (Casablanca)
- 🇰🇪 Kenya (Nairobi)
- 🇬🇭 Ghana (Accra)
- 🇿🇦 South Africa (Johannesburg)
- 🇺🇸 USA (New York)
- 🇪🇹 Ethiopia (Addis Ababa)

---

## 🗄️ Database Schema

### `flights`
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Auto-increment PK |
| flight_number | TEXT | e.g. BA072 |
| airline | TEXT | e.g. British Airways |
| origin | TEXT | Departure city |
| destination | TEXT | Arrival city |
| departure_time | TEXT | e.g. 09:15 |
| arrival_time | TEXT | e.g. 15:55 |
| duration | TEXT | e.g. 6h 40m |
| economy_price | REAL | Base price/pax |
| business_price | REAL | Business price/pax |
| first_price | REAL | First class price/pax |
| total_seats | INTEGER | Aircraft capacity |
| available_seats | INTEGER | Remaining seats |
| aircraft | TEXT | e.g. Boeing 777 |

### `bookings`
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Auto-increment PK |
| booking_ref | TEXT | Unique ref e.g. SKY-A3F9-X2 |
| flight_id | INTEGER | FK → flights.id |
| travel_date | TEXT | Date of travel |
| flight_class | TEXT | Economy/Business/First Class |
| total_passengers | INTEGER | Number of pax |
| total_price | REAL | Final price paid |
| status | TEXT | Confirmed / Cancelled |

### `passengers`
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Auto-increment PK |
| booking_ref | TEXT | FK → bookings.booking_ref |
| first_name | TEXT | |
| last_name | TEXT | |
| passport_number | TEXT | |
| date_of_birth | TEXT | YYYY-MM-DD |
| nationality | TEXT | |
| seat_number | TEXT | e.g. 15C |

---

## 🖥️ UI Screenshots Description

### 🏠 Home Page
- Dark deep-navy background with glowing radial gradient accents
- Large hero section with animated gradient title "Your Journey Begins Here ✈️"
- 4 stats cards: Destinations · Bookings · Airlines · Support
- 6 popular-route cards in a 3-column grid
- 3 feature cards (Safe & Reliable, Best Price, Instant Booking)

### 🔍 Search Flights
- Form with dropdowns for city, class, date picker, and passenger count
- Results rendered as styled "flight cards" with departure/arrival times,
  airline logo emoji, price, seats remaining, and a Select button
- After selecting: passenger form with name, passport, DOB, seat, nationality
- Price summary box with surge-pricing notice for last-minute bookings
- Booking confirmation screen with large reference code on success

### 📋 My Booking
- Text input for booking reference
- Full booking summary card + per-passenger detail cards
- Monospace-styled E-ticket with download button

### 🛡️ Admin Panel
- PIN login screen
- 5 stat cards: Total · Confirmed · Cancelled · Revenue · Top Route
- 3 tabs: All Bookings (sortable table) · All Flights (full schedule) · Cancel Booking

---

## ⚡ Pricing Logic

- **Base price** is per passenger (from the flights table for the selected class)
- **Last-minute surcharge**: +25% if travel date is ≤ 7 days away
- **Total** = base_price × passengers × surge_multiplier

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| UI Framework | Streamlit 1.35+ |
| Database | SQLite3 (Python built-in) |
| Data Display | Pandas DataFrames |
| Styling | Custom CSS via `st.markdown()` |
| Fonts | Google Fonts — Sora + DM Sans |
| Python | 3.10+ standard library |

---

## 📚 Learning Points

This project demonstrates:
- **OOP-ready module structure** — each `.py` file has a single responsibility
- **SQLite CRUD** — CREATE, READ, UPDATE, DELETE with parameterised queries (safe from SQL injection)
- **Session state management** — using `st.session_state` to persist data across Streamlit reruns
- **Form validation** — server-side checks on passenger input before writing to DB
- **Dynamic UI** — generating cards, seat maps, and tickets programmatically from DB data
- **Custom CSS in Streamlit** — overriding default styles with injected HTML/CSS

---

## 🔐 Security Notes (for production)

1. Change the admin PIN or replace with a proper auth system
2. Hash passport numbers before storing
3. Use environment variables for secrets (`python-dotenv`)
4. Add HTTPS if deploying publicly (Streamlit Cloud handles this automatically)

---

*Built with ❤️ using Python + Streamlit · Skyline Airways © 2025*
