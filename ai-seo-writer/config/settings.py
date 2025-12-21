import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    
    # Validation constraints
    MAX_KEYWORD_WORDS = 6
    
    @staticmethod
    def validate():
        if not Config.GEMINI_API_KEY:
             print("Warning: GEMINI_API_KEY not found in environment variables.")

# Auto-validate on import mostly for simple scripts, 
# but in a larger app we might want explicit validation.
Config.validate()
