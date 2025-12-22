from luma.core.interface.serial import spi
from luma.lcd.device import ili9341
from PIL import Image, ImageDraw, ImageFont
import RPi.GPIO as GPIO
import time
import os
import threading

# Load icon image
icon_path = os.path.join(os.path.dirname(__file__), "icon.png")
if os.path.exists(icon_path):
    icon_img = Image.open(icon_path).convert("RGBA")
    icon_img = icon_img.resize((20, 20), Image.LANCZOS)
else:
    icon_img = None
    
def init_lcd():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(26, GPIO.OUT)
    GPIO.output(26, GPIO.HIGH)
    serial = spi(port=0, device=0, gpio_DC=25, gpio_RST=24)
    device = ili9341(serial, rotate=0)

    font = ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        14
    )

    return device, font

# Battery percentage handler
def battery_percentage_handler(battery_percentage):
    global battery_percent
    battery_percent = int(battery_percentage.get('percentage', 0))

# LumaLCD functions
def update_battery(device, img, font, timeout=2.0):
        """
        Fetches the latest battery percentage from the RVR and updates the display.
        """
        global battery_percent

        # Request new battery percentage
        battery_percent = None
        rvr.get_battery_percentage(handler=battery_percentage_handler)

        # Wait for response (up to timeout seconds)
        start = time.time()
        while battery_percent is None and (time.time() - start) < timeout:
            time.sleep(0.05)

        # If no response, default to 0
        current_percent = battery_percent if battery_percent is not None else 0

        # Determine which battery image to use
        base_path = os.path.join(os.path.dirname(__file__), "batteries")
        if current_percent <= 25:
            battery_img_path = os.path.join(base_path, "lowbattery.png")
        elif current_percent <= 50:
            battery_img_path = os.path.join(base_path, "midbattery.png")
        elif current_percent <= 75:
            battery_img_path = os.path.join(base_path, "decentbattery.png")
        else:
            battery_img_path = os.path.join(base_path, "fullbattery.png")

        battery_icon = Image.open(battery_img_path).convert("RGBA")
        battery_icon = battery_icon.rotate(-90, expand=True)
        battery_icon = battery_icon.resize((40, 20))

        # Clear previous battery area
        draw = ImageDraw.Draw(img)
        icon_x = img.width - battery_icon.width - 10
        icon_y = 10
        draw.rectangle((icon_x - 50, icon_y - 5, img.width, icon_y + battery_icon.height + 5), fill="black")

        # Paste icon and draw percentage text
        img.paste(battery_icon, (icon_x, icon_y), battery_icon)
        text = f"{current_percent}%"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        text_x = icon_x - text_width - 5
        text_y = icon_y + (battery_icon.height - text_height) // 2
        draw.text((text_x, text_y), text, font=font, fill="white")

        # Update display
        device.display(img)

def draw_centered_text(draw, img, text, font, fill="white", y_offset=0):
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        text_x = (img.width - text_width) // 2
        text_y = (img.height - text_height) // 2 + y_offset
        draw.text((text_x, text_y), text, font=font, fill=fill)

def show_centered_message(text, delay=1.5):
        img = Image.new("RGB", device.size, "black")
        draw = ImageDraw.Draw(img)
        # Draw Plant Monitor Demo in top-left
        draw.text((10, 10), "Plant Monitor Demo", font=font, fill="white")
        update_battery(device, img, font)
        draw_centered_text(draw, img, text, font)
        device.display(img)
        time.sleep(delay)

def show_loading_screen(device, font, message="Loading..."):
    # Create blank screen first
    img = Image.new("RGB", device.size, "black")
    draw = ImageDraw.Draw(img)

    # --- Header drawing ---
    x_offset = 10
    y_offset = 10

    # Icon (if present)
    if icon_img:
        img.paste(icon_img, (x_offset, y_offset), icon_img)
        x_offset += icon_img.width + 5

    # Title
    draw.text((x_offset, y_offset), "Plant Monitor Demo", font=font, fill="white")

    # Right-side text
    right_text = "3991-1"
    bbox = draw.textbbox((0, 0), right_text, font=font)
    text_width = bbox[2] - bbox[0]
    draw.text((img.width - text_width - 10, y_offset), right_text, font=font, fill="white")

    # --- Center message ---
    bbox = draw.textbbox((0, 0), message, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = (img.width - text_width) // 2
    text_y = (img.height - text_height) // 2
    draw.text((text_x, text_y), message, font=font, fill="white")

    device.display(img)