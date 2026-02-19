"""
  RavensPi, 2025-2026
  Module/File: pump.py
"""
# libaries
import RPi.GPIO as GPIO
import time

# pin
PUMP_PIN = 13 

# setup gpio
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(PUMP_PIN, GPIO.OUT)

# main function
def pump_water(duration=1):
    print("Pumping water...")
    GPIO.output(PUMP_PIN, GPIO.HIGH)
    time.sleep(duration)
    GPIO.output(PUMP_PIN, GPIO.LOW)
    time.sleep(0.5)
    print("Watering done")