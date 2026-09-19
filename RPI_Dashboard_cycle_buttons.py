#!/usr/bin/env python3

import subprocess
import time
from gpiozero import Button

# ============================================================
# DASHBOARDS
# ============================================================

DASHBOARDS = [
    ("MarineTraffic", "https://www.marinetraffic.com/"),
    ("FlightRadar24", "https://www.flightradar24.com/"),
    ("Windy", "https://www.windy.com/"),
    ("GridStatus MISO", "https://www.gridstatus.io/live/miso"),
    ("NASA", "https://www.nasa.gov/")
]

# ============================================================
# GPIO BUTTONS
# ============================================================

# GPIO pin numbers, NOT physical pin numbers
next_button = Button(17, bounce_time=0.2)
prev_button = Button(27, bounce_time=0.2)
home_button = Button(22, bounce_time=0.2)

# ============================================================
# DASHBOARD STATE
# ============================================================

current = 0
chromium = None


def start_dashboard(index):
    global chromium

    name, url = DASHBOARDS[index]

    print(f"Opening: {name}")
    print(f"URL: {url}")

    # Close the current Chromium instance
    if chromium is not None:
        try:
            chromium.terminate()
            chromium.wait(timeout=3)
        except Exception:
            try:
                chromium.kill()
            except Exception:
                pass

        time.sleep(1)

 # Start the new dashboard
    chromium = subprocess.Popen([
        "/usr/bin/chromium",
        "--kiosk",
        "--noerrdialogs",
        "--disable-infobars",
        "--disable-session-crashed-bubble",
        url
    ])


def next_dashboard():
    global current

    current = (current + 1) % len(DASHBOARDS)
    start_dashboard(current)


def previous_dashboard():
    global current

    current = (current - 1) % len(DASHBOARDS)
    start_dashboard(current)


def home_dashboard():
    global current

    current = 0
    start_dashboard(current)


# ============================================================
# BUTTON ACTIONS
# ============================================================

next_button.when_pressed = next_dashboard
prev_button.when_pressed = previous_dashboard
home_button.when_pressed = home_dashboard


# ============================================================
# START
# ============================================================

print("===================================")
print(" Raspberry Pi Dashboard Controller ")
print("===================================")
print("NEXT  = GPIO 17")
print("PREV  = GPIO 27")
print("HOME  = GPIO 22")
print("-----------------------------------")

start_dashboard(current)

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("\nStopping dashboard...")

finally:
    if chromium is not None:
        try:
            chromium.terminate()
        except Exception:
            pass

    next_button.close()
    prev_button.close()
    home_button.close()

