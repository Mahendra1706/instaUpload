from instagrapi import Client
from dotenv import load_dotenv
import os

# Load env vars
load_dotenv()

def upload_to_instagram(video_path: str, caption: str = "New Reel Uploaded"):
    cl = Client()

    username = os.getenv("INSTA_USERNAME")
    password = os.getenv("INSTA_PASSWORD")

    # First time login
    try:
        cl.load_settings("settings.json")  # Load previous session
    except:
        print("No settings.json found. Starting fresh login.")

    try:
        cl.login(username, password)
        cl.dump_settings("settings.json")  # Save session
    except Exception as e:
        print(" Login failed:", e)
        return {"error": str(e)}

    try:
        cl.clip_upload(video_path, caption)
        print("✅ Uploaded to Instagram")
        return {"status": "success"}
    except Exception as e:
        print(" Upload failed:", e)
        return {"error": str(e)}
