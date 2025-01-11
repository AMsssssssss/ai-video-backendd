
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import shutil
import os
import moviepy.editor as mp
from moviepy.video.fx.all import crop

app = FastAPI()

UPLOAD_DIR = "uploads"
PROCESSED_DIR = "processed"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

@app.post("/upload/")
async def upload_video(file: UploadFile = File(...)):
    file_location = f"{UPLOAD_DIR}/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"message": "Upload successful", "filename": file.filename}

def crop_to_vertical(input_video, output_video):
    video = mp.VideoFileClip(input_video)
    width, height = video.size
    new_width = height * 9 / 16
    x1 = (width - new_width) / 2
    x2 = x1 + new_width
    cropped = crop(video, x1=x1, y1=0, x2=x2, y2=height)
    cropped.write_videofile(output_video, codec='libx264', audio_codec='aac')

def extract_highlight(input_video, output_video):
    video = mp.VideoFileClip(input_video)
    highlight = video.subclip(0, min(10, video.duration))
    highlight.write_videofile(output_video, codec='libx264', audio_codec='aac')

@app.post("/process/")
async def process_video(filename: str):
    input_path = f"{UPLOAD_DIR}/{filename}"
    processed_path = f"{PROCESSED_DIR}/processed_{filename}"
    crop_to_vertical(input_path, processed_path)
    extract_highlight(processed_path, processed_path)
    return {"message": "Processing complete", "processed_file": f"/download/{filename}"}

@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = f"{PROCESSED_DIR}/processed_{filename}"
    return FileResponse(file_path, media_type="video/mp4", filename=f"short_{filename}")

if __name__ == "__main__":
    import uvicorn
    import os
    
    port = int(os.environ.get("PORT", 8000))  # Use the port Render assigns
    uvicorn.run("main:app", host="0.0.0.0", port=port)    
