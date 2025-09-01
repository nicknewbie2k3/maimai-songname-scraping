import json
import time
import pyautogui  # Make sure to install pyautogui: pip install pyautogui
import os
import pyperclip  # Add this: pip install pyperclip

def input_message_macro(prompt_text="Enter your message: "):
    """
    Prompts the user for a message and formats it for sending.
    """
    message = input(prompt_text)
    return message

def send_message_macro(message):
    """
    Mimics user input by pasting the message (supports non-English characters) and pressing Enter.
    """
    pyperclip.copy(message)
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press('enter')

# Fix the path to point to the parent directory
json_path = os.path.join(os.path.dirname(__file__), '..', 'maimai-songName.json')
# Load the JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Loop through each element and send the message
for song in data:
    song_name = song.get('title', 'Unknown')
    message = f'm>info {song_name}'
    send_message_macro(message)  # This will paste and send the message
    time.sleep(2)

# Example usage:
if __name__ == "__main__":
    msg = input_message_macro()
    send_message_macro(msg)

