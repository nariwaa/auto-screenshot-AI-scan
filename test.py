import threading
import ollama
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path

file_path = "/home/ayaya/Screenshots/2025-02-05-100659_hyprshot.png"

# Configuration
SCREENSHOT_DIR = "/home/ayaya/Screenshots/"
MODEL_NAME = "llama3.2-vision:11b"
ANALYSIS_PROMPT = "Analyze this screenshot and describe its contents. Be concise."
# OLLAMA_HOST = "http://192.168.1.122:11434"
OLLAMA_HOST = "http://127.0.0.1:11434"

# Create custom client with proper initialization
client = ollama.Client(host=OLLAMA_HOST)
# Create a lock to serialize requests
request_lock = threading.Lock()

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
    print("\nWaiting for new screenshots...")

except Exception as e:
    print(f"Error processing {file_path}: {str(e)}")
