"""
  RavensPi, 2025-2026
  Module/File: rvrfunctions.py
  Note: Contains both RVR movement and distance sensor functions
"""

# Libaries
from turtle import speed

from sphero_sdk import *
import time
import threading
import qwiic_vl53l1x
import sys


# Define RVR and LED control
rvr = SpheroRvrObserver()
leds = LedControlObserver(rvr)

# Rear LED full red (stopped)
def rear_red_full():
    leds.set_led_color(RvrLedGroups.brakelight_left, Colors.red)
    leds.set_led_color(RvrLedGroups.brakelight_right, Colors.red)

# Rear LED dim red (moving)
def rear_red_low():
    leds.set_led_rgb(RvrLedGroups.brakelight_left, 128, 0, 0)
    leds.set_led_rgb(RvrLedGroups.brakelight_right, 128, 0, 0)
    
# Front headlights white
def front_white():
    leds.set_led_color(RvrLedGroups.headlight_left, Colors.white)
    leds.set_led_color(RvrLedGroups.headlight_right, Colors.white)

def init_tof(tries=3):
    global tof
    for trial in range(tries):
        tof = qwiic_vl53l1x.QwiicVL53L1X()
        try:
            if tof.sensor_init() is None:
                print("VL53L1X distance sensor online")
                return True
            else:
                print(f"VL53L1X init failed (attempt {trial + 1}/3)")
        except OSError as e:
            print(f"VL53L1X I2C error (attempt {trial + 1}/3): {e}")
        time.sleep(0.5)  # wait before retry

    print("VL53L1X failed after 3 attempts, exiting")
    sys.exit(1)

# Uses threading to blink turn signals while turning
def blink_turn_signal(led_group, rear, times=2, interval=0.5):
    def blink():
        for _ in range(times):
            leds.set_led_color(led_group, Colors.yellow)
            leds.set_led_color(rear, Colors.orange)
            time.sleep(interval)
            leds.set_led_color(led_group, Colors.off)
            leds.set_led_color(rear, Colors.off)
            time.sleep(interval)
        leds.set_led_color(led_group, Colors.white)
    threading.Thread(target=blink, daemon=True).start()

# Turn off all LEDs
def all_lights_off():
    leds.turn_leds_off()

# Turn left with blinking signal
def turn_left_with_signal(amount):
    rvr.drive_control.reset_heading()
    blink_turn_signal(RvrLedGroups.headlight_left, RvrLedGroups.brakelight_left)
    rvr.drive_control.turn_left_degrees(heading=0, amount=amount)
    time.sleep(2)
    front_white()
    rear_red_full()


# Turn right with blinking signal
def turn_right_with_signal(amount):
    rvr.drive_control.reset_heading()
    blink_turn_signal(RvrLedGroups.headlight_right, RvrLedGroups.brakelight_right)
    rvr.drive_control.turn_right_degrees(heading=0, amount=amount)
    time.sleep(2)
    front_white()
    rear_red_full()
    time.sleep(1)
    rear_red_low()


# Drive forward in milliseconds
def drive_forward(milliseconds, speed=40):
    rvr.reset_yaw()
    rear_red_low()
    seconds = milliseconds / 1000.0
    rvr.drive_control.drive_forward_seconds(
        speed=speed,
        heading=0,
        time_to_drive=seconds
    )
    rear_red_full()
    time.sleep(1)

# Drive backward in milliseconds
def drive_backward(milliseconds, speed=40):
    rvr.reset_yaw()
    rear_red_low()
    seconds = milliseconds / 1000.0
    rvr.drive_control.drive_backward_seconds(
        speed=speed,
        heading=0,
        time_to_drive=seconds
    )
    rear_red_full()
    time.sleep(1)

def get_distance(retries=3):
    for attempt in range(retries):
        try:
            time.sleep(0.005)
            distance = tof.get_distance()
            time.sleep(0.005)
            tof.clear_interrupt()  # arm for next read
            if distance is not None and distance > 0:
                return distance
            print(f"Bad read on attempt {attempt + 1}, retrying...")
            
        except Exception as e:
            print(f"Sensor error: {e}")
    print("All retries failed")
    return None

# Move forward to target distance using distance sensor
def move_forward_to_distance(target_mm, speed=40, tolerance_mm=5):
    rvr.reset_yaw()
    rear_red_low()
    tof.start_ranging()
    time.sleep(0.3)
    for _ in range(3):
        tof.get_distance()
        tof.clear_interrupt()
        time.sleep(0.01)
    
    rvr.drive_control.roll_start(speed=100, heading=0)
    time.sleep(0.1)
    rvr.drive_control.roll_start(speed=speed, heading=0)

    try:
        while True:
            current_mm = get_distance()

            if current_mm is None:
                print("Bad sensor read, stopping")
                break

            print(f"Distance: {current_mm}mm -> target: {target_mm}mm")

            if current_mm <= target_mm + tolerance_mm:
                print("Target reached")
                break

            gap = current_mm - target_mm
            if gap < 100:
                scaled_speed = 15
            else:
                scaled_speed = max(20, min(speed, int(speed * (gap / 200))))

            rvr.drive_control.roll_start(speed=scaled_speed, heading=0)
            time.sleep(0.05)

    finally:
        rvr.drive_control.roll_stop(0)
        tof.stop_ranging()
        rear_red_full()


# Move backward to target distance using distance sensor
def move_backward_to_distance(target_mm, speed=30, tolerance_mm=5):
    rvr.reset_yaw()        
    rear_red_low()
    tof.start_ranging()
    time.sleep(0.3)
    
    for _ in range(3):
        tof.get_distance()
        tof.clear_interrupt()
        time.sleep(0.01)
        
    rvr.drive_control.roll_start(speed=-100, heading=0)
    time.sleep(0.1)
    rvr.drive_control.roll_start(speed=-speed, heading=0)

    try:
        while True:
            current_mm = get_distance()

            if current_mm is None:
                print("Bad sensor read, stopping")
                break

            print(f"Distance: {current_mm}mm -> target: {target_mm}mm")

            if current_mm >= target_mm - tolerance_mm:
                print("Target reached")
                break

            gap = target_mm - current_mm
            if gap < 100:
                scaled_speed = 15
            else:
                scaled_speed = max(20, min(speed, int(speed * (gap / 200))))

            rvr.drive_control.roll_start(speed=-scaled_speed, heading=0)
            time.sleep(0.05)

    finally:
        rvr.drive_control.roll_stop(0)
        tof.stop_ranging()
        rear_red_full()
        
        
# Note: used code from both the Sphero RVR SDK and Sparkfun VL53L1X Library for reference