"""
  RavensPi, 2025-2026
  Module/File: rvrfunctions.py
  Note: Contains both RVR movement and distance sensor functions
"""

# Imports
from sphero_sdk import *
import time
import threading
import qwiic_vl53l1x

tof = None

# Define RVR and LED control
rvr = SpheroRvrObserver()
leds = LedControlObserver(rvr)

#Rear LED full red (stopped)
def rear_red_full():
    leds.set_led_color(RvrLedGroups.brakelight_left, Colors.red)
    leds.set_led_color(RvrLedGroups.brakelight_right, Colors.red)

#Rear LED dim red (moving)
def rear_red_low():
    leds.set_led_rgb(RvrLedGroups.brakelight_left, 128, 0, 0)
    leds.set_led_rgb(RvrLedGroups.brakelight_right, 128, 0, 0)
    
#Front headlights white
def front_white():
    leds.set_led_color(RvrLedGroups.headlight_left, Colors.white)
    leds.set_led_color(RvrLedGroups.headlight_right, Colors.white)

def init_tof():
    global tof
    tof = qwiic_vl53l1x.QwiicVL53L1X()
    try:
        if tof.sensor_init() is None:
            print("VL53L1X distance sensor online")
            return True
        else:
            print("VL53L1X init failed")
            return False
    except OSError as e:
        print(f"VL53L1X I2C error: {e}")
        return False

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
def drive_forward(milliseconds, speed=25):
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
def drive_backward(milliseconds, speed=25):
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

# Get distance from distance sensor and print
def get_distance():
    tof.start_ranging()
    time.sleep(0.005)
    distance = tof.get_distance()
    time.sleep(0.005)
    tof.stop_ranging()
    return distance


# Move forward to target distance using distance sensor
def move_forward_to_distance(target_mm, step_mm=5, speed=25, tolerance_mm=2, max_steps=50):
    rvr.reset_yaw()
    rear_red_low()
    tof.start_ranging()
    try:
        steps = 0
        current_mm = get_distance()
        # Check if too close:
        if current_mm <= target_mm + tolerance_mm:
            print("Too close, skipping move forward")
            return

        while True:
            current_mm = get_distance()
            if abs(current_mm - target_mm) <= tolerance_mm:
                break
            if current_mm < target_mm:
                print("Too close, stopping")
                break
            if steps >= max_steps:
                print("Timeout: max steps reached")
                break

            step_time = step_mm / 152.4  
            rvr.reset_yaw()
            rvr.drive_control.drive_forward_seconds(speed=speed, heading=0, time_to_drive=step_time)
            steps += 1

    finally:
        tof.stop_ranging()
        rear_red_full()
        time.sleep(0.2)


# Move away from target distance using distance sensor
def move_backward_to_distance(target_mm, step_mm=5, speed=30, tolerance_mm=2, max_steps=50):
    rvr.reset_yaw()
    rear_red_low()
    tof.start_ranging()
    try:
        steps = 0
        current_mm = get_distance()
        # Check if already too far:
        if current_mm >= target_mm - tolerance_mm:
            print("Too far, skipping move backward")
            return

        while True:
            current_mm = get_distance()
            if abs(current_mm - target_mm) <= tolerance_mm:
                break
            if current_mm > target_mm:
                print("Too far, stopping")
                break
            if steps >= max_steps:
                print("Timeout: max steps reached")
                break

            step_time = step_mm / 152.4
            rvr.reset_yaw()
            rvr.drive_control.drive_backward_seconds(speed=speed, heading=0, time_to_drive=step_time)
            steps += 1

    finally:
        tof.stop_ranging()
        rear_red_full()
        time.sleep(0.2)
        
# Note: used code from both the Sphero RVR SDK and Sparkfun VL53L1X Library for reference