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