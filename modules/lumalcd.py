"""
  RavensPi, 2025-2026
  Module/File: lumalcd.py
"""

# Imports
from luma.core.interface.serial import spi
from luma.lcd.device import ili9341
from PIL import Image, ImageDraw, ImageFont
import RPi.GPIO as GPIO
import os

# Load RavensPi logo
icon_path = os.path.join(os.path.dirname(__file__), "icon.png")
if os.path.exists(icon_path):
    icon_img = Image.open(icon_path).convert("RGBA")
    icon_img = icon_img.resize((20, 20), Image.LANCZOS)
else:
    icon_img = None

# Initialize LCD
def init_lcd():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(26, GPIO.OUT)
    GPIO.output(26, GPIO.HIGH)
    serial = spi(port=0, device=0, gpio_DC=25, gpio_RST=24)
    device = ili9341(serial, rotate=0)
    # Choose font and size
    font = ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        14
    )

    return device, font

# Main function
def show_information(device, font, message):
    # Create blank screen
    img = Image.new("RGB", device.size, "black")
    draw = ImageDraw.Draw(img)

    # Header for the header on the top
    x_offset = 10
    y_offset = 10

    # Icon
    if icon_img:
        img.paste(icon_img, (x_offset, y_offset), icon_img)
        x_offset += icon_img.width + 5

    # Title
    draw.text((x_offset, y_offset), "RavensPi", font=font, fill="white")

    # Right-side text
    right_text = "3991-1"
    bbox = draw.textbbox((0, 0), right_text, font=font)
    text_width = bbox[2] - bbox[0]
    draw.text((img.width - text_width - 10, y_offset), right_text, font=font, fill="white")

    # Center message
    bbox = draw.textbbox((0, 0), message, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = (img.width - text_width) // 2
    text_y = (img.height - text_height) // 2
    draw.text((text_x, text_y), message, font=font, fill="white")

    device.display(img) # displays the img