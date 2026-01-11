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
from modules.pump import *


init_tof() 
init_servos()
time.sleep(1)

# Start program with button hold
show_information(device, font, message="Ready. Hold button for 1 second to start.")
hold_to_start()
show_information(device, font, message="Starting...")


def send_to_GPT(image_path=None):
  from modules.xiao import readline
  soil_percent = readline() 
  report = analyze_plant(soil_percent, image_path)
  return report



# Main loop for plant
def check_plant(plant_id):
  image_path = capture_plant_image() # take photo
  time.sleep(1)
  turn_left_with_signal(90) # turn toward plant
  print("Before moving forward")
  get_distance()
  move_forward_to_distance(40) # drive forward to plant
  print("After moving forward")
  get_distance()
  move_servo(75) # insert sensor
  report = send_to_GPT(image_path=image_path) # get report
  slowly_move_servo(150) # remove sensor
  pump_water(1) # water plant
  print("Before moving backward")
  get_distance()
  move_backward_to_distance(165) # drive backward to route
  print("After moving backward")
  get_distance()
  turn_right_with_signal(90) # turn back to route
  time.sleep(1)
  return report

plant1 = check_plant(1)
drive_forward(1150)
plant2 = check_plant(2)
drive_forward(1150)
plant3 = check_plant(3)

print("Report of Plant 1:\n", plant1.encode('utf-8', errors='replace').decode('utf-8'))
print("Report of Plant 2:\n", plant2.encode('utf-8', errors='replace').decode('utf-8'))
print("Report of Plant 3:\n", plant3.encode('utf-8', errors='replace').decode('utf-8'))
print("Sending email...")
show_information(device, font, message="Sending...")
send_email(plant1=plant1, plant2=plant2, plant3=plant3)

show_information(device, font, message="Finished.")