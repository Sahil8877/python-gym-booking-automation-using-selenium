# 🚀 Gym Booking Automation System

A Python-based **end-to-end browser automation system** built with Selenium to automate gym class discovery, booking, and verification workflows on a live web application.

This project simulates real-world **workflow automation, system interaction, and transactional validation**, similar to production support automation tools used in enterprise environments.

---

## 📌 Key Features

- 🔐 Automated login handling with retry logic and session persistence
- 📅 Dynamic parsing of gym schedules across multiple days
- 🎯 Intelligent filtering of classes based on time (e.g. 6:00 PM sessions)
- 🟢 Automated booking and waitlist handling based on real-time UI state
- 🔁 Robust retry mechanism for unstable UI interactions
- ⚠️ Exception handling for stale elements and missing DOM nodes
- ✅ Post-action verification via booking confirmation page
- 📊 Booking consistency validation between source and target pages

---

## 🧠 System Architecture

Gym Landing Page  
        ↓  
Login Automation Layer  
        ↓  
Schedule Scraping Engine  
        ↓  
Class Filtering Logic (Time-based rules)  
        ↓  
Booking Engine (Book / Waitlist / Skip)  
        ↓  
Verification Layer (My Bookings Page)  

This project follows a **multi-stage workflow pipeline**, similar to event-driven automation systems used in production environments.

---

## ⚙️ Tech Stack

- Python 3.x
- Selenium WebDriver
- ChromeDriver
- WebDriverWait (Explicit waits)
- HTML DOM parsing
- Exception handling & retry logic

---

## 🧩 Core Functional Modules

### 1. Authentication Automation
Handles login workflow with retry support for unstable UI interactions.

- Input automation for credentials
- Form submission handling
- URL validation after authentication

---

### 2. Schedule Extraction Engine
Parses dynamic DOM structure to extract:

- Class names
- Time slots
- Availability status
- Booking button state
- Day/date grouping

---

### 3. Booking Decision Engine

Implements rule-based automation logic:

- Book class if available
- Join waitlist if required
- Skip if already booked/waitlisted
- Handles real-time UI state changes (`aria-busy` detection)

---

### 4. Resilient Automation Layer

- Retry wrapper for failed actions
- Handles:
  - `StaleElementReferenceException`
  - `NoSuchElementException`
- Ensures workflow continuity under UI instability

---

### 5. Verification & Validation Layer

- Navigates to “My Bookings” page
- Extracts confirmed and waitlisted sessions
- Validates expected vs actual bookings
- Logs discrepancies for debugging

---

## 📊 Example Output

Booked: Yoga Class on Tue 5 May, at 6:00 PM
Waitlisted: HIIT Class on Thu 7 May, at 6:00 PM

--- VERIFICATION RESULT ---
Expected: 4 bookings
Found: 4 bookings
✅ SUCCESS: All bookings verified!
---

## 🧠 Engineering Concepts Demonstrated

This project demonstrates skills directly transferable to **Application Support / Production Support roles**:

- Workflow automation & orchestration
- Real-time UI state handling
- Exception handling & system resilience
- Multi-step transaction processing
- Data extraction from dynamic systems
- End-to-end process validation
- Retry logic for unstable environments

---

## 🚀 Why This Project Matters

Unlike basic automation scripts, this project simulates:

- Multi-step business workflows
- Real-world system dependency handling
- Failure recovery mechanisms
- Post-process validation (critical in production systems)

It reflects how production support engineers:
> diagnose → automate → validate → ensure system consistency

---

## 🔧 Possible Enhancements

- Add logging framework (`logging`)
- Introduce configuration management (`.env`)
- Store bookings in a database (SQLite/PostgreSQL)
- Add API wrapper layer
- Convert retry logic into decorators
- Implement scheduling (cron / GitHub Actions)
- Add notification system (email/Slack alerts)

---

## 📁 Project Structure
python-gym-booking-automation-using-selenium
|-main.py
|-readme.md
