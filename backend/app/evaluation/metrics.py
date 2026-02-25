import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent 
PROJECT_ROOT = BASE_DIR.parent                    
ENV_PATH = PROJECT_ROOT / ".env"

load_dotenv(dotenv_path=ENV_PATH)

groq_api_key = os.getenv("GROQ_API_KEY")
langsmith_api_key = os.getenv("LANGSMITH_API_KEY")

if groq_api_key is None or langsmith_api_key is None:
    raise EnvironmentError("GROQ_API_KEY or LANGSMITH_API_KEY not set in environment")

os.environ["LANGSMITH_TRACING"] = "true"