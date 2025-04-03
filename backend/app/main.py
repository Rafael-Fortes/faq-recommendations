from fastapi import FastAPI
from app.routes import gestion_routes, search_routes
from dotenv import load_dotenv
from app.utils.logger import Logger

load_dotenv()

Logger.info("Starting the application")
app = FastAPI()


app.include_router(gestion_routes.router)
app.include_router(search_routes.router)
Logger.info("Application started")