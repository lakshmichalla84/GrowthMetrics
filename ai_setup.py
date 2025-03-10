import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("API key is missing. Please set the GEMINI_API_KEY.")

genai.configure(api_key=api_key)

def process_observation(observation):
    try:
        model = genai.GenerativeModel("gemini-1.5-pro", generation_config={"temperature": 0.0})
        response = model.generate_content(observation)
        
        if response.text:
            return {
                'content': response.text,
                'finished_reason': response.candidates[0].finish_reason if response.candidates else None
            }
        else:
            raise ValueError("No response generated")
    
    except Exception as e:
        raise RuntimeError(f"Error processing observation: {str(e)}")