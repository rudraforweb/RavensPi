from sphero_sdk import *
import time
import threading
import math

rvr = SpheroRvrObserver()
leds = LedControlObserver(rvr)

def rear_red_full():
    """Rear LED full red (stopped)"""
    leds.set_led_color(RvrLedGroups.brakelight_left, Colors.red)
    leds.set_led_color(RvrLedGroups.brakelight_right, Colors.red)

def rear_red_low():
    """Rear LED dim red (moving)"""
    leds.set_led_rgb(RvrLedGroups.brakelight_left, 128, 0, 0)
    leds.set_led_rgb(RvrLedGroups.brakelight_right, 128, 0, 0)

def front_white():
    """Front headlights white"""
    leds.set_led_color(RvrLedGroups.headlight_left, Colors.white)
    leds.set_led_color(RvrLedGroups.headlight_right, Colors.white)

def blink_turn_signal(led_group, rear, times=2, interval=0.5):
    """Blinks a turn signal LED asynchronously and restores color to white when done."""
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

def all_lights_off():
    """Turn off all LEDs"""
    leds.turn_leds_off()

def turn_left_with_signal(amount):
    """Turn left while blinking left signal"""
    rvr.drive_control.reset_heading()
    blink_turn_signal(RvrLedGroups.headlight_left, RvrLedGroups.brakelight_left)
    rvr.drive_control.turn_left_degrees(heading=0, amount=amount)
    time.sleep(2)
    front_white()
    rear_red_full()



def turn_right_with_signal(amount):
    """Turn right while blinking right signal"""
    rvr.drive_control.reset_heading()
    blink_turn_signal(RvrLedGroups.headlight_right, RvrLedGroups.brakelight_right)
    rvr.drive_control.turn_right_degrees(heading=0, amount=amount)
    time.sleep(2)
    front_white()
    rear_red_full()
    time.sleep(1)
    rear_red_low()


def drive_forward(milliseconds, speed=32):
    """Drive forward with dim rear lights, then stop with full red.
    Time input is in milliseconds.
    """
    rear_red_low()
    seconds = milliseconds / 1000.0
    rvr.drive_control.drive_forward_seconds(
        speed=speed,
        heading=0,
        time_to_drive=seconds
    )
    rear_red_full()
    time.sleep(1)

def drive_backward(milliseconds, speed=32):
    """Drive backward with dim rear lights, then stop with full red.
    Time input is in milliseconds.
    """
    rear_red_low()
    seconds = milliseconds / 1000.0
    rvr.drive_control.drive_backward_seconds(
        speed=speed,
        heading=0,
        time_to_drive=seconds
    )
    rear_red_full()
    time.sleep(1)