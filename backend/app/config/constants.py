import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.environ.get("MONGO_URI")


if not MONGO_URI:
    raise ValueError("MONGO_URI is not set")

