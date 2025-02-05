import threading
import ollama
import os
import time
from pathlib import Path
from typing import Optional

# Configuration
MODEL_NAME = "llava:7b"
# MODEL_NAME = "llama3.2-vision:11b"

OLLAMA_HOST = "http://192.168.1.122:11434"
# OLLAMA_HOST = "http://127.0.0.1:11434"

ANALYSIS_PROMPT = "Analyze this screenshot and describe its contents. Be concise."
SCREENSHOT_DIR = "/home/ayaya/Screenshots/"

# Code

client = ollama.Client(host=OLLAMA_HOST)
request_lock = threading.Lock()

def processimg(file_path):
    try:
        response = client.chat(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": ANALYSIS_PROMPT,
                    "images": [str(file_path)]
                }
            ]
        )

        print("\nAnalysis Result:")
        print(response['message']['content'])

    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")


def imgpath(last_path: Optional[str] = None) -> str:
    """
    Wait until a new screenshot is detected in the SCREENSHOT_DIR directory.
    
    Args:
        last_path: Path of the previously detected screenshot
        
    Returns:
        Full path of the new screenshot when found
    """
    while True:
        try:
            # Get all files in the directory
            files = Path(SCREENSHOT_DIR).glob('*')
            
            # Filter for image files and get the most recent one
            image_extensions = ('.png', '.jpg', '.jpeg', '.gif')
            latest_screenshot = max(
                (f for f in files if f.suffix.lower() in image_extensions),
                key=lambda x: x.stat().st_mtime,
                default=None
            )
            
            if latest_screenshot is not None:
                latest_path = str(latest_screenshot.absolute())
                
                # If this is a new screenshot, return its path
                if last_path != latest_path:
                    return latest_path
            
            # Wait a bit before checking again
            time.sleep(0.5)
            
        except Exception as e:
            print(f"Error checking for screenshots: {e}")
            time.sleep(1)  # Wait longer if there's an error

# main loop
while True:
    print("ready!")
    processimg(imgpath(imgpath()))
    print("\nWaiting for new screenshots...")

