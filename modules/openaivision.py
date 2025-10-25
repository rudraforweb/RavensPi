def encode_image(image_path):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image '{image_path}' not found.")
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode('utf-8')

photos_dir = "photos"
os.makedirs(photos_dir, exist_ok=True)
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
image_path = os.path.join(photos_dir, f"photo_{timestamp}.jpg")

# Maximum resolution for Raspberry Pi Camera Module 2: 3280x2464
max_width, max_height = 3280, 2464
square_size = 2464  # Crop to 2464x2464 (centered square)
raw_image_path = os.path.join(photos_dir, f"photo_{timestamp}_raw.jpg")

picam2 = Picamera2()
# Configure camera for max resolution
camera_config = picam2.create_still_configuration(main={"size": (max_width, max_height)})
picam2.configure(camera_config)
picam2.start()
picam2.capture_file(raw_image_path)
picam2.close()

# Crop to center square (2464x2464)
with Image.open(raw_image_path) as img:
    width, height = img.size
    left = (width - square_size) // 2
    top = (height - square_size) // 2
    right = left + square_size
    bottom = top + square_size
    img_cropped = img.crop((left, top, right, bottom))
    img_cropped.save(image_path)

prompt_text = "Analyze this plant's health in detail. Describe the leaf color, shape, and texture. Note any signs of wilting, yellowing, browning, spots, pests, or dryness. Based on these observations, explain if the plant appears healthy or unhealthy, and recommend whether it needs watering, more sunlight, fertilizer, or other care. Limit your response to 2 sentences."

def generate_plant_report():
    try:
        base64_image = encode_image(image_path)

        client = OpenAI(api_key="place_your_openai_api_key_here")

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

        print("\nGPT-4o-mini says:\n")
        print(response.choices[0].message.content)

        # Cleanup: delete raw_image_path and image_path files
        for file_path in [raw_image_path, image_path]:
            try:
                os.remove(file_path)
            except Exception:
                pass

    except Exception as e:
        print(f"Error: {e}")