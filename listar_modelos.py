import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_KEY:
    print("❌ Error: No encontré GEMINI_API_KEY en .env")
    exit()

genai.configure(api_key=GEMINI_KEY)

print("\n🔍 Modelos disponibles en tu API Key:\n")

try:
    for model in genai.list_models():
        if "generateContent" in model.supported_generation_methods:
            print(f"✅ {model.name}")
            print(f"   Descripción: {model.display_name}")
            print()
except Exception as e:
    print(f"❌ Error: {e}")
