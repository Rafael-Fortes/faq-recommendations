import os
from dotenv import load_dotenv

load_dotenv()

QDRANT_URL = os.environ.get("QDRANT_URL")

if not QDRANT_URL:
    raise ValueError("QDRANT_URL is not set in the environment variables")

