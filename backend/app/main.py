from fastapi import FastAPI
from app.routes import gestion_routes
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.include_router(gestion_routes.router)
