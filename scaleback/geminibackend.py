import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# 1. This magically finds your .env file and loads the key into memory
load_dotenv()

# 2. Grab the key securely from memory
MY_API_KEY = os.environ.get("GEMINI_API_KEY")

# 3. Configure the AI
if not MY_API_KEY:
    print("⚠️ ERROR: Could not find GEMINI_API_KEY in the .env file!")
else:
    genai.configure(api_key=MY_API_KEY)

def analyze_meal(user_input: str) -> dict:
    # ... (The rest of your parsing logic stays exactly the same)
    """
    Takes natural language food input and returns structured macro data.
    """
    
    # 1. The System Prompt: Setting the rules of engagement
    system_instruction = """
    You are a headless nutritional analysis API. 
    Calculate the nutritional values for the user's meal. 
    Assume standard Indian portion sizes if not specified (e.g., standard size roti, medium bowl of dal).
    
    You MUST return ONLY a valid JSON object. No conversational text. No markdown formatting.
    
    The JSON must follow this exact schema:
    {
        "calories": <integer>,
        "protein": <integer>,
        "carbs": <integer>,
        "fats": <integer>,
        "fibers": <integers>,
        "logged_items": ["list", "of", "items"]
    }
    """

    # 2. Model Initialization (Flash is perfectly fast and cheap for this)
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction=system_instruction
    )

    try:
        # 3. The API Call with JSON Enforcement
        response = model.generate_content(
            user_input,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json", # Forces JSON output
                temperature=0.1 # Keep it deterministic, we want math, not creativity
            )
        )
        
        # Parse the string response into a Python dictionary
        macro_data = json.loads(response.text)
        return macro_data

    except Exception as e:
        print(f"Pipeline Error: {e}")
        # Fallback empty state so the app doesn't crash
        return {"calories": 0, "protein": 0, "carbs": 0, "fats": 0, "logged_items": []}

# --- Let's test the Vibe ---
if __name__ == "__main__":
    test_input = "I just ate 3 rotis, a cup of dal makhani, and a scoop of whey protein in water"
    result = analyze_meal(test_input)
    
    print("User Typed:", test_input)
    print("Database Ready Output:")
    print(json.dumps(result, indent=2))