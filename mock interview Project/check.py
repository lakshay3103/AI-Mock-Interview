import google.generativeai as genai

# PASTE YOUR KEY HERE
API_KEY = "AIzaSyD2RboTJKzy7v7u2uzSCBB-AgBqvD6O6R8"
genai.configure(api_key=API_KEY)

print("--- CONTACTING GOOGLE ---")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"FOUND: {m.name}")
except Exception as e:
    print(f"ERROR: {e}")