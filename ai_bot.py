import os
import time
import google.generativeai as genai
from pytchat import create
import sys

# API Keys (GitHub Secrets se automatic connect hongi)
GEMINI_KEY = os.environ.get("GEMINI_KEY")
YT_API_KEY = os.environ.get("YT_API_KEY")

# APNI CHANNEL ID YAHAN DALO (Example: UCxxxxxxxxxxxxxxx)
# Ye aapko YouTube Studio -> Settings -> Advanced mein milegi
CHANNEL_ID = "EUiBEBPJFpS04Yj4" 

# Gemini AI Setup
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-pro')

def get_ai_reply(text):
    try:
        # AI ko chota reply dene ka instruction
        response = model.generate_content(f"Reply in 1 very short Hinglish sentence: {text}")
        return response.text
    except Exception as e:
        return "AI abhi busy hai, thoda ruko!"

def start_bot():
    print(f"Searching for Live Chat on Channel: {CHANNEL_ID}")
    try:
        # Channel ID se connect karne ka fayda: Video ID badalne par bhi bot chalta rahega
        chat = create(channel_id=CHANNEL_ID)
        
        if chat.is_alive():
            print("--- Success! AI Bot Connected via Channel ---")
            while chat.is_alive():
                for c in chat.get().sync_items():
                    if c.message.startswith("!ai"):
                        query = c.message.replace("!ai", "").strip()
                        reply = get_ai_reply(query)
                        
                        # Logs mein reply print karega (Action Console mein)
                        print(f"\nUser: {c.author.name}\nQuery: {query}\nAI Reply: {reply}")
                        print("-" * 30)
                time.sleep(1)
        else:
            print("Bot ko live stream nahi mili. Check karein ki stream PUBLIC hai.")
            # 30 seconds baad auto-retry karega
            time.sleep(30)
            start_bot()
            
    except Exception as e:
        print(f"Connection Error: {e}")
        time.sleep(30)
        start_bot()

if __name__ == "__main__":
    start_bot()
