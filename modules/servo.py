"""
  RavensPi, 2025-2026
  File: servo.py
"""

# Imports
from adafruit_servokit import ServoKit
import time

# Define servo kit
kit = ServoKit(channels=16)

# Define servo for soil moisture sensor
servo = kit.servo[0]
servo_channel = 0

# Main function: step is degrees per step, delay is time between steps
def move_servo(target_angle, step=3, delay=0.02):
    # Start from current angle, or 0 if undefined
    current_angle = kit.servo[servo_channel].angle
    if current_angle is None:
        current_angle = 0

    # Determine direction of motion:
    if current_angle < target_angle:
        angles = range(int(current_angle), int(target_angle)+1, step) # Servo is below target: step forward
    else:
        angles = range(int(current_angle), int(target_angle)-1, -step) # Servo is above target: step back

    # Move servo to each value in range
    for angle in angles:
        kit.servo[servo_channel].angle = angle
        time.sleep(delay)

    # Final angle set
    kit.servo[servo_channel].angle = target_angle