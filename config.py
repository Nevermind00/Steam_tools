import dotenv
import os

dotenv.load_dotenv()
steam_token = os.getenv("API_KEY")
DB_NAME = "wishlist.db"
if not steam_token:
    raise ValueError("STEAM_TOKEN is not defined in environment variables or .env file")