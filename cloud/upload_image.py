import os
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader

# Load variables from .env
load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("CLOUD_NAME"),
    api_key=os.getenv("API_KEY"),
    api_secret=os.getenv("API_SECRET")
)


def upload_image(image_path):

    try:

        result = cloudinary.uploader.upload(image_path)

        print("✅ Image uploaded to Cloudinary")

        return result["secure_url"]

    except Exception as e:

        print("❌ Upload Failed")

        print(e)

        return None