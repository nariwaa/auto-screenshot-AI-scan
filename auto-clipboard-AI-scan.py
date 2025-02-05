import threading
import ollama
import time
import subprocess
from typing import Optional

# Configuration
MODEL_NAME = "deepseek-r1:8b"
OLLAMA_HOST = "http://192.168.1.122:11434"
PROMPT_PREFIX = "solve this: "
CHECK_INTERVAL = 0.5  # Seconds between clipboard checks

# Code
client = ollama.Client(host=OLLAMA_HOST)

def get_clipboard_content() -> Optional[str]:
    """Get text content from Wayland clipboard using wl-paste"""
    try:
        content = subprocess.check_output(['wl-paste'],
                                         stderr=subprocess.DEVNULL).decode().strip()
        return content if content else None
    except subprocess.CalledProcessError:
        return None
    except Exception as e:
        print(f"Error accessing clipboard: {str(e)}")
        return None

def process_text(text: str):
    """Process text with the LLM model"""
    print(f"Processing new clipboard content...\n")
    try:
        response = client.chat(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": PROMPT_PREFIX + text
                }
            ]
        )

        print("\nAnalysis Result:")
        print(response['message']['content'])

    except Exception as e:
        print(f"Error processing text: {str(e)}")

def monitor_clipboard(initial_content: Optional[str] = None):
    """Monitor clipboard for new content"""
    last_clipboard_content = initial_content if initial_content is not None else None
    
    while True:
        current_content = get_clipboard_content()

        if current_content and current_content != last_clipboard_content:
            last_clipboard_content = current_content
            process_text(current_content)
            print("\nMonitoring clipboard...")

        time.sleep(CHECK_INTERVAL)

# Main execution
if __name__ == "__main__":
    print("Clipboard monitor ready!")

    # Get initial clipboard content to avoid processing on startup
    initial_clipboard_content = get_clipboard_content()

    try:
        monitor_clipboard(initial_clipboard_content)
    except KeyboardInterrupt:
        print("\nExiting...")
