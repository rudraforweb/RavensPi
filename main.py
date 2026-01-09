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
from modules.openaivision import *
show_information(device, font, message="Loading other services...")
from modules.servo import *
from modules.qwiicbutton import *
from modules.xiao import *
from modules.email import *


# use XIAO output as soil moisture percentage

# Start program with button hold
show_information(device, font, message="Ready. Hold button for 1 second to start.")
hold_to_start()
show_information(device, font, message="Starting...")


def send_to_GPT():
  from modules.xiao import readline
  soil_percent = readline() 
  report = analyze_plant(soil_percent)
  return report

plant1 = send_to_GPT()
print(plant1)
plant2 = send_to_GPT()
print(plant2)
plant3 = send_to_GPT()
print(plant3)
print("Sending email...")
send_email(plant1=plant1, plant2=plant2, plant3=plant3)
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
'''
show_information(device, font, message="Finished.")