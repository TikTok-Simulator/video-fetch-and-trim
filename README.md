# Video Fetch and Trim
This repository provides a Python script to fetch videos from the Hugging Face finevideo dataset, filter them by category, and process them by trimming to a random duration. The processed videos and their metadata are saved locally for further use.

# Instructions to Run `main.py`

1. **Install Requirements**  
    Run the following command to install the required dependencies:  
    ```bash
    pip3 install -r requirements.txt
    ```

2. **Set Up Environment Variables**  
    Create a `.env` file in the project directory and add these necessary variables:
    ```env
    HUGGING_FACE_TOKEN=
    CATEGORY=
    MAX_VIDEOS_PER_CATEGORY=
    ```
    Note: Token can be retrieved from https://huggingface.co/settings/tokens

3. **Run the Script**  
    Execute the script using:  
    ```bash
    python3 main.py
    ```  

# Explain
- Get videos from dataset (streaming mode) -> filters videos based on a specific category -> trims them to a random duration (10-20s) -> saves both the trimmed videos and their metadata

- The trimmed videos are saved in the `videos` directory with filenames like `<category>_<index>.mp4`. Metadata files are named similarly to the videos: `<category>_<index>.json`

# List of categories:
- Education
- Entertainment
- Automotive
- Art & Creativity
- Sports
- Hobbies & Interests
- News & Politics
- Lifestyle
- Science & Technology