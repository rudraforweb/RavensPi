"""
  RavensPi, 2025-2026
  File: servo.py
"""

from adafruit_servokit import ServoKit
import time

kit = ServoKit(channels=16)

servo = kit.servo[0]  # channel 0
servo_channel = 0

kit = ServoKit(channels=16)
servo_channel = 0

def move_servo_slowly(target_angle, step=3, delay=0.02):
    # Start from current angle, default 0 if unknown
    current_angle = kit.servo[servo_channel].angle
    if current_angle is None:
        current_angle = 0

    # Make a range list to iterate over (avoids while loops getting stuck)
    if current_angle < target_angle:
        angles = range(int(current_angle), int(target_angle)+1, step)
    else:
        angles = range(int(current_angle), int(target_angle)-1, -step)

    for angle in angles:
        kit.servo[servo_channel].angle = angle
        time.sleep(delay)

    kit.servo[servo_channel].angle = target_angle