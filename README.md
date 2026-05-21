# 🚀 Gym Booking Automation System

A Selenium based end-to-end automation project that simulates a structured gym booking workflow with validation, retry mechanisms, and dynamic UI handling on the [App Brewery gym demo app](https://appbrewery.github.io/gym/).

The project demonstrates browser automation, state based decision logic, and resilient workflow execution using Python and Selenium.

---

## ⚡ At a Glance

| | |
|---|---|
| 🔧 | Automates full gym booking flow: login → schedule → booking → verification |
| 🧠 | Parses dynamic DOM to extract class schedules grouped by day |
| 🎯 | Filters and books all Tuesday & Thursday 6:00 PM sessions |
| 🔁 | Wraps key actions in a retry loop (up to 7 attempts) |
| ✅ | Cross-validates bookings on the My Bookings confirmation page |

---

## 📌 Key Features

- 🔐 **Automated login** with credential input, form submission, and URL based success validation
- 📅 **Day grouped schedule parsing** — targets `div[id^='day-group-']` elements, filtered by `tue` / `thu`
- 🎯 **6:00 PM class filtering** across both target days
- 🟢 **Smart booking engine** — handles `Book Class`, `Join Waitlist`, `Booked`, and `Waitlisted` button states
- ⏳ **`aria-busy` polling** — waits for button state to resolve before proceeding
- 🔁 **Generic `retry()` wrapper** — retries any callable up to N times on falsy return
- ⚠️ **Exception handling** for `StaleElementReferenceException` and `NoSuchElementException`
- ✅ **Post-booking verification** — compares expected vs. actual count across confirmed and waitlisted bookings
- 🧩 **Persistent Chrome profile** — uses a local `gym_profile/` directory to preserve session state

---

## 🧠 Workflow Pipeline

```
https://appbrewery.github.io/gym/
        ↓
Click "Join Today" → redirect to /login/
        ↓
Login Automation  (retry up to 7x, validates redirect to /schedule/)
        ↓
Schedule DOM Parsing  (day-groups filtered by 'tue' / 'thu')
        ↓
Class Filtering  (time == '6:00 PM')
        ↓
Booking Engine  (Book / Join Waitlist / Skip if already handled)
        ↓  aria-busy polling after each click
Verification  (/my-bookings/ — confirmed + waitlisted count vs. expected)
```

---

## ⚙️ Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.x | Core scripting language |
| Selenium WebDriver | Browser automation |
| ChromeDriver | Chrome browser interface |
| `WebDriverWait` + `EC` | Explicit wait strategies |
| `StaleElementReferenceException` handling | DOM re-query on element loss |
| Persistent Chrome profile | Session and cookie persistence across runs |

---

## 🧩 Code Structure

This project is implemented as a **single script** (`main.py`) organised into focused functions:

```
main.py
├── Chrome setup          # Options, detach mode, persistent profile, driver init
├── retry(func, descr)    # Generic retry wrapper — retries any callable up to N times
├── login()               # Credential input, form submit, URL validation
├── Schedule parsing      # DOM traversal: day-groups → class metadata → `classes[]`
├── book_class()          # Booking logic with aria-busy polling and state handling
└── verify_booking()      # Navigates to /my-bookings/, counts and cross-validates
```

> All booking state is tracked in the `classes[]` list and the `total_6pm_classes` counter, which is passed implicitly into `verify_booking()`.

---

## 🔁 Retry Logic

```python
def retry(func, descr, retries=7):
    for attempt in range(1, retries + 1):
        if func():
            return True
        print(descr + f" Attempt : {attempt}")
    print("⚠️ Re-attempt failed while : ", descr)
    return False
```

Any function that returns `True` on success and `False` on failure can be passed into `retry()`. Used for both `login()` and `book_class()`.

---

## 🎯 Booking Decision Logic

For each 6:00 PM class, the engine reads the live button text and acts accordingly:

| Button State | Action |
|---|---|
| `Book Class` | Click → poll `aria-busy` → confirm `Booked` |
| `Join Waitlist` | Click → poll `aria-busy` → confirm `Waitlisted` |
| `Booked` | Skip — already handled, increment counter |
| `Waitlisted` | Skip — already handled, increment counter |
| Unknown | Log warning, continue |

---

## 📊 Example Output

```text
Booked:      Yoga Class   — Tue 6 May, 6:00 PM
Waitlisted:  HIIT Class   — Thu 8 May, 6:00 PM

--- Total Tuesday/Thursday 6pm classes: 4 ---

--- VERIFYING ON MY BOOKINGS PAGE ---
  ✓ Verified: Yoga Class
  ✓ Verified: Pilates Class
  ✓ Verified: HIIT Class
  ✓ Verified: Spin Class

--- VERIFICATION RESULT ---
Expected : 4 bookings
Found    : 4 bookings
✅ SUCCESS: All bookings verified!
```

---

## 🚀 Getting Started

```bash
# Clone the repository
git clone https://github.com/your-username/gym-booking-automation.git
cd gym-booking-automation

# Install dependencies
pip install selenium

# Run the script
python main.py
```

> ⚠️ Ensure ChromeDriver is installed and matches your installed Chrome version. A `gym_profile/` directory will be created automatically on first run to persist your session.
