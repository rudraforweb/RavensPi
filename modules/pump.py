import RPi.GPIO as GPIO
import time

# GPIO pin connected to MOSFET gate
PUMP_PIN = 13 

# Setup pins once at module load (after setting mode)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(PUMP_PIN, GPIO.OUT)


def pump_water(duration=1):
    print("Pumping water...")
    GPIO.output(PUMP_PIN, GPIO.HIGH)
    time.sleep(duration)
    GPIO.output(PUMP_PIN, GPIO.LOW)
    time.sleep(0.5)
    print("Watering done")