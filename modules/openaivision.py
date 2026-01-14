"""
  RavensPi, 2025-2026
  Module/File: openaivision.py
"""

# Imports
from picamera2 import Picamera2
import datetime
from openai import OpenAI
import base64
import os
from PIL import Image


# Encode image to base64
def encode_image(image_path):
    if not os.path.exists(image_path): # Check for image
        raise FileNotFoundError(f"Image '{image_path}' not found.")
    with open(image_path, "rb") as f: # Encode
        return base64.b64encode(f.read()).decode('utf-8')

# Photo directory
photos_dir = "photos"
os.makedirs(photos_dir, exist_ok=True)

# Take photo
def take_photo():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S") # Timestamp
    image_path = os.path.join(photos_dir, f"photo_{timestamp}.jpg") # Image path

    max_width, max_height = 3280, 2464 # Resolution of Raspberry Pi Camera v2

    # Capture image
    picam2 = Picamera2()
    camera_config = picam2.create_still_configuration(main={"size": (max_width, max_height)})
    picam2.configure(camera_config)
    picam2.start()
    picam2.capture_file(image_path)
    picam2.close()

    return image_path

# Generate plant report
def generate_plant_report(image_path, soil_percent):
    try:
        prompt_text = f"Analyze this plant's health in detail. Soil moisture is {soil_percent:.1f}%, say Soil Moisture is (the soil moisture), in your response. Describe the leaf color, shape, and texture. Note any signs of wilting, yellowing, browning, spots, pests, or dryness. Based on these observations, explain if the plant appears healthy or unhealthy. Limit your response to 2 sentences."

        base64_image = encode_image(image_path)

        client = OpenAI(api_key="") # VALID OPENAI KEY REQUIRED

        # send image and prompt to GPT-4o-mini
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt_text},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=300
        )


        # cleanup
        try:
            os.remove(image_path)
        except Exception:
            pass
            
        return response.choices[0].message.content

    except Exception as e:
        print(f"Error: {e}")

def capture_plant_image():
    image_path = take_photo()
    return image_path

# Main function
def analyze_plant(soil_percent, image_path):
    report = generate_plant_report(image_path, soil_percent)
    return report