# from fastapi import FastAPI, Request
# from pydantic import BaseModel
# from typing import List, Union
# from yt_dlp import YoutubeDL
# from datetime import datetime
# from utils.instaupload import upload_to_instagram

# app = FastAPI()

# class ReelInput(BaseModel):
#     url: str

# @app.post("/download")
# async def download_reels(request: Request):
#     try:
#         json_data = await request.json()

#         # If it's a dict, make it a list with one item
#         if isinstance(json_data, dict):
#             json_data = [json_data]

#         reels = [ReelInput(**item) for item in json_data]

#         for item in reels:
#             url = item.url
#             if not url:
#                 continue

#             timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#             filename = f"reel_{timestamp}.%(ext)s"

#             ydl_opts = {
#                 'outtmpl': filename,
#                 'format': 'mp4',
#                 'verbose': True,
#             }

#             print(f"Downloading from: {url}")
#             with YoutubeDL(ydl_opts) as ydl:
#                 ydl.download([url])
#             print("✅ Downloaded successfully")

#         return {"message": "All reels processed"}

#     except Exception as e:
#         return {"error": str(e)}

from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List
from yt_dlp import YoutubeDL
from datetime import datetime
# from utils.instaupload import upload_to_instagram  
from utils.instaupload import upload_to_instagram


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
            result = upload_to_instagram(final_video_filename, caption=" Auto-uploaded reel")
            print(result)

        return {"message": "All reels processed and uploaded!"}

    except Exception as e:
        return {"error": str(e)}

