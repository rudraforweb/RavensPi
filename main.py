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
from modules.rvrfunctions import rvr, leds
rvr.wake()
time.sleep(1)
print("RVR Awake")

# Import remaining modules after loading screen and RVR attempt
from modules.rvrfunctions import *
show_loading_screen(device, font, message="Loading GPT vision...")
#from modules.openaivision import *
show_loading_screen(device, font, message="Loading other services...")
from modules.servo import *
from modules.qwiicbutton import *
from modules.xiao import *
from modules.email import *


# Start program with button hold
show_loading_screen(device, font, message="Ready. Hold button for 1 second to start.")
hold_to_start()
show_loading_screen(device, font, message="Starting...")
'''
# example loop
for i in range(3):
  drive_forward(1300) # inital drive forward
  # INSERT: take camera picture
  turn_left_with_signal(90) # turn toward plant
  drive_forward(600) # drive forward to plant
  # INSERT: inject soil moisture sensor into soil
  # INSERT: send both data to GPT-4o for analysis
  # INSERT: get GPT-4o response and water plant based on response
  time.sleep(1) 
  drive_backward(600) # drive backward to route
  turn_right_with_signal(90) # turn back to route
'''
def check_plant():
  # INSERT: take camera picture
  turn_left_with_signal(90) # turn toward plant
  drive_forward(600) # drive forward to plant
  # INSERT: inject soil moisture sensor into soil
  # INSERT: send both data to GPT-4o for analysis
  # INSERT: get GPT-4o response and water plant based on response
  time.sleep(1) 
  drive_backward(600) # drive backward to route
  turn_right_with_signal(90) # turn back to route

check_plant()
drive_forward(1000)
check_plant()
drive_forward(1000)
check_plant()