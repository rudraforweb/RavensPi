"""
  RavensPi, 2025-2026
  Team ID: 3991-1
  Team Members: Rudra Kumar, Benjamin Leonard, and Dean Forsyth
  Robofest Exhibition
  Sunlake Academy of Math and Science
  File: main.py
"""
# Inital imports
import time
from modules.lumalcd import *

# Initialize LCD and RVR, and show loading screen
device, font = init_lcd()
show_information(device, font, message="Starting RVR...")
from modules.rvrfunctions import rvr # Import RVR for wake
rvr.wake()
time.sleep(1)
print("RVR Awake")

# Import remaining modules after loading screen and RVR attempt
from modules.rvrfunctions import * # Import rest of RVR functions
show_information(device, font, message="Loading GPT vision...")
#from modules.openaivision import *
show_information(device, font, message="Loading other services...")
from modules.servo import *
from modules.qwiicbutton import *
from modules.xiao import *
from modules.email import *

# Start program with button hold
'''
show_information(device, font, message="Ready. Hold button for 1 second to start.")
hold_to_start()
show_information(device, font, message="Starting...")
'''


# Main loop for plant
def check_plant():
  # INSERT: take camera picture
  turn_left_with_signal(90) # turn toward plant
  print("Before moving forward")
  get_distance()
  move_forward_to_distance(50) # drive forward to plant
  print("After moving forward")
  get_distance()
  # INSERT: inject soil moisture sensor into soil
  # INSERT: send both data to GPT-4o for analysis
  # INSERT: get GPT-4o response and water plant based on response
  time.sleep(1) 
  print("Before moving backward")
  get_distance()
  move_backward_to_distance(175) # drive backward to route
  print("After moving backward")
  get_distance()
  turn_right_with_signal(90) # turn back to route
  time.sleep(1)

check_plant()
drive_forward(1250)
check_plant()
drive_forward(1250)
check_plant()