"""
  RavensPi, 2025-2026
  File: servo.py
"""

# Imports
from adafruit_servokit import ServoKit
import time

# variables
kit = None
servo_channel = 0

def init_servos(channels=16):
    """Initialize the ServoKit and define the servo channel."""
    global kit, servo_channel
    kit = ServoKit(channels=channels)
    servo_channel = 0 

# Main function: move servo directly to target angle
def move_servo(target_angle):
    global kit, servo_channel
    if kit is None:
        raise RuntimeError("ServoKit not initialized. Call init_servos() first.")
    kit.servo[servo_channel].angle = target_angle

# Slowly move the servo from its current angle to the target angle using steps
def slowly_move_servo(target_angle, step=1, delay=0.02):
    global kit, servo_channel
    if kit is None:
        raise RuntimeError("ServoKit not initialized. Call init_servos() first.")

    current_angle = kit.servo[servo_channel].angle

    if current_angle is None:
        kit.servo[servo_channel].angle = target_angle
        return

    if current_angle < target_angle:
        angles = range(int(current_angle), int(target_angle) + 1, step)
    else:
        angles = range(int(current_angle), int(target_angle) - 1, -step)

    for angle in angles:
        kit.servo[servo_channel].angle = angle
        time.sleep(delay)

    kit.servo[servo_channel].angle = target_angle