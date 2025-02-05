# deepseek did that and it's broken... 
import threading
import ollama
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path

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

class ScreenshotHandler(FileSystemEventHandler):
    def __init__(self):
        self.processed_files = set()

    def on_created(self, event):
        if event.is_directory or not event.src_path.endswith(".png"):
            return
            
        file_path = Path(event.src_path)
        if str(file_path) in self.processed_files:
            return

        print(f"\nNew screenshot detected: {file_path.name}")
        # Use the lock to ensure only one request is processed at a time.
        with request_lock:
            self.process_screenshot(file_path)
        self.processed_files.add(str(file_path))

    def process_screenshot(self, file_path: Path):
        try:
            if not file_path.exists():
                raise FileNotFoundError(f"File {file_path} disappeared")

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

def check_ollama_connection():
    try:
        # Simple ping to verify connection
        response = client.generate(model=MODEL_NAME, prompt="ping")
        return True
    except Exception as e:
        print(f"Connection failed: {str(e)}")
        print("Verify:\n1. Server running\n2. Host/port correct\n3. Firewall allows access")
        return False

if __name__ == "__main__":
    if not check_ollama_connection():
        exit(1)

    event_handler = ScreenshotHandler()
    observer = Observer()
    observer.schedule(event_handler, SCREENSHOT_DIR, recursive=False)
    observer.start()

    print(f"Monitoring {SCREENSHOT_DIR} for new screenshots...")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
