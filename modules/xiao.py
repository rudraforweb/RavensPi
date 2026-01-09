"""
  RavensPi, 2025-2026
  Module/File: xiao.py
"""

# Imports
import serial
import time

# Read soil moisture sensor data from XIAO
def readline():
    # Open serial connection to XIAO
    ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
    time.sleep(2)  # allow XIAO to reset

    ser.flush()

    dry_air = 850
    wet_water = 315

    while True:
        # Read one line from XIAO
        line = ser.readline().decode().strip()
        if line:
            try:
                value = float(line)
                # Calculate percentage
                percentage = (dry_air - value) / (dry_air - wet_water) * 100
                # Clamp between 0 and 100
                percentage = max(0, min(100, percentage))
                print("Value:", value)
                print("Percentage:", percentage)
                return percentage
            except ValueError:
                print("Received non-numeric data from XIAO, retrying...")
        else:
            print("No response received from XIAO, retrying...")