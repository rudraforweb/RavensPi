"""
  RavensPi, 2025-2026
  Team ID: 3991-1
  Team Members: Rudra Kumar, Benjamin Leonard, and Dean Forsyth
  Robofest Exhibition
  Sunlake Academy of Math and Science
  File: main.py
"""

import time
from modules.lumalcd import init_lcd, show_loading_screen

# Initialize LCD and show loading screen
device, font = init_lcd()
show_loading_screen(device, font, message="Starting RVR...")
from sphero_sdk import SpheroRvrObserver, LedControlObserver
rvr = SpheroRvrObserver()
leds = LedControlObserver(rvr)

rvr.wake()
time.sleep(1)
print("RVR Awake")

# Import remaining modules after loading screen and RVR attempt
from modules.rvrfunctions import *
show_loading_screen(device, font, message="Loading GPT vision...")
from modules.openaivision import *
show_loading_screen(device, font, message="Loading other services...")
from modules.servo import *
from modules.qwiicbutton import *
from modules.xiao import *
from modules.email import *
time.sleep(1)

# Start program with button hold
show_loading_screen(device, font, message="Ready. Hold button for 1 second to start.")
hold_to_start()
show_loading_screen(device, font, message="Starting...")