from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List
from yt_dlp import YoutubeDL
from datetime import datetime
# from utils.instaupload import upload_to_instagram  
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils.instaupload import upload_to_instagram

# Fallback function if import fails
def upload_to_instagram_fallback(video_path: str, caption: str = "New Reel Uploaded"):
    try:
        from instagrapi import Client
        from dotenv import load_dotenv
        import os
        
        # Load env vars
        load_dotenv()
        
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
    except ImportError:
        print("Instagram upload dependencies not available, skipping upload")
        return {"status": "skipped", "reason": "dependencies not available"}
    except Exception as e:
        print("Upload error:", e)
        return {"error": str(e)}


app = FastAPI()



class ReelInput(BaseModel):
    url: str

@app.post("/download")
async def download_reels(request: Request):
    try:
        json_data = await request.json()

        # Support both single object and list of objects
        if isinstance(json_data, dict):
            json_data = [json_data]

        reels = [ReelInput(**item) for item in json_data]

        for item in reels:
            url = item.url
            if not url:
                continue

            # Timestamped filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"reel_{timestamp}.%(ext)s"
            final_video_filename = f"reel_{timestamp}.mp4"

            ydl_opts = {
                'outtmpl': filename,
                'format': 'mp4',
                'verbose': True,
            }

            print(f" Downloading from: {url}")
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            print(f" Downloaded as {final_video_filename}")

            # 🔺 Upload to Instagram
            print("Uploading to Instagram...")
            try:
                result = upload_to_instagram(final_video_filename, caption=" Auto-uploaded reel")
            except:
                result = upload_to_instagram_fallback(final_video_filename, caption=" Auto-uploaded reel")
            print(result)

        return {"message": "All reels processed and uploaded!"}

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("reels:app", host="0.0.0.0", port=8000, reload=True)


