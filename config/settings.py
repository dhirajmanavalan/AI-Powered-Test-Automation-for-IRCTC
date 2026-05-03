import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

class Settings:

    MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
    MISTRAL_MODEL = os.getenv("MISTRAL_MODEL")

settings = Settings()
