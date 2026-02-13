import os
import time
import google.generativeai as genai
from pytchat import create
import sys

# API Setup
GEMINI_KEY = os.environ.get("GEMINI_KEY")
# CHANNEL_ID yahan UC se shuru hone wali dalo
CHANNEL_ID = "UCSdDJgyrqtcSi3GeqLGb6GA" 

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-pro')

def start_bot():
    print(f"Connecting to Channel Chat: {CHANNEL_ID}")
    try:
        chat = create(channel_id=CHANNEL_ID)
        if not chat.is_alive():
            print("Chat is not active. Retrying...")
            time.sleep(10)
            return start_bot()

        print("--- AI Bot Connected and Running ---")
        while chat.is_alive():
            for c in chat.get().sync_items():
                if c.message.startswith("!ai"):
                    query = c.message.replace("!ai", "").strip()
                    try:
                        response = model.generate_content(f"Reply in 1 short Hinglish sentence: {query}")
                        print(f"User: {c.author.name} | AI: {response.text}")
                    except:
                        print("AI limit hit, skipping...")
            time.sleep(1)
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(10)
        start_bot()

if __name__ == "__main__":
    start_bot()
