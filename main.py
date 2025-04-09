from datasets import load_dataset
import json
import os
from huggingface_hub import login
from moviepy.video.io.VideoFileClip import VideoFileClip
from io import BytesIO
import random
import tempfile
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)
HUGGING_FACE_TOKEN = os.getenv("HUGGING_FACE_TOKEN")
CATEGORY = os.getenv("CATEGORY", "undefined")
MAX_VIDEOS_PER_CATEGORY = int(os.getenv("MAX_VIDEOS_PER_CATEGORY", 100))
print("Downloading videos from category:", CATEGORY)

login(HUGGING_FACE_TOKEN)

# Load dataset (streaming mode)
dataset = load_dataset("HuggingFaceFV/finevideo", split="train", streaming=True)


def is_desired_category(sample):
    return sample["json"]["content_parent_category"] == CATEGORY


filtered_dataset = filter(is_desired_category, dataset)

# Create directories (save videos and metadata)
VIDEO_DIR = "videos"
METADATA_DIR = "metadata"
os.makedirs(VIDEO_DIR, exist_ok=True)
os.makedirs(METADATA_DIR, exist_ok=True)

for idx, sample in enumerate(filtered_dataset):
    if idx >= MAX_VIDEOS_PER_CATEGORY:
        break

    # Load video from bytes & Save video bytes to a temporary file
    video_bytes = BytesIO(sample["mp4"])
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video_file:
        temp_video_file.write(video_bytes.read())
        temp_video_path = temp_video_file.name

    try:
        with VideoFileClip(temp_video_path) as video:
            duration = video.duration

            # Generate random start and end times for trimming
            if duration > 20:
                start_time = random.uniform(0, duration - 20)
                end_time = start_time + random.uniform(10, 20)
                end_time = min(end_time, duration)

                trimmed_video = video.subclipped(start_time, end_time)
            else:
                trimmed_video = video

            video_filename = f"{VIDEO_DIR}/{CATEGORY.lower()}_{idx}.mp4"
            trimmed_video.write_videofile(
                video_filename, codec="libx264", audio_codec="aac"
            )

        # Save metadata
        custom_metadata = {
            "category": sample["json"]["content_parent_category"],
            "description": sample["json"]["content_metadata"]["description"],
            "length": trimmed_video.duration,
        }
        json_filename = f"{METADATA_DIR}/{CATEGORY.lower()}_{idx}.json"
        with open(json_filename, "w") as json_file:
            json.dump(custom_metadata, json_file)
    finally:
        # Clean up temporary file
        os.remove(temp_video_path)
