
"""
  RavensPi, 2025-2026
  Module/File: qwiicbutton.py
"""

import qwiic_button
import time
import sys

brightness = 100

def hold_to_start():

    my_button = qwiic_button.QwiicButton()

    if my_button.begin() == False:
        print("\nThe Qwiic Button isn't connected.", \
            file=sys.stderr)
        return
    
    print("\nReady to start. Hold the button for 1 second to begin.")

    # Pulse LED variables
    brightness = 250    
    cycle_time = 1000  
    off_time = 0        

    # Start pulsing:
    my_button.LED_config(brightness, cycle_time, off_time)

    press_count = 0
    hold_start = 0

    while True:
        if my_button.is_button_pressed():
            if press_count == 0:
                hold_start = time.time()
            press_count = 1
            if time.time() - hold_start >= 1.0:  # held for at least 1 second
                my_button.LED_on(255)
                break
        else:
            press_count = 0

        time.sleep(0.1)
        
        
# Note: used code from Sparkfun Qwiic Button Python Library for reference