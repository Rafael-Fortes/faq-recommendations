# FAQ Recommendations Backend

## Purpose

This is the backend application for the FAQ Recommendations project. It provides the API and services for FAQ management, search functionality, and recommendation generation. Built with FastAPI and Python, it leverages vector database technology (Qdrant) for semantic search capabilities and efficient FAQ retrieval based on user queries.

## Folder Structure

```
backend/
├── .cursor/             # Cursor IDE configuration
├── .venv/               # Python virtual environment
├── app/                 # Source code
│   ├── config/          # Configuration settings
│   ├── core/            # Core application logic
│   ├── db/              # Database models and connections
│   ├── routes/          # API route definitions
│   ├── schemas/         # Pydantic data models
│   ├── services/        # Business logic services
│   ├── utils/           # Utility functions
│   ├── __init__.py      # Package initialization
│   └── main.py          # Application entry point
├── qdrant_storage/      # Vector database storage files
├── .dockerignore        # Files to exclude from Docker builds
├── .env                 # Environment variables
├── .env-example         # Example environment configuration
├── .gitignore           # Git ignore configuration
├── .python-version      # Python version specification
├── Dockerfile           # Docker configuration
├── docker-compose.yml   # Multi-container Docker configuration
├── poetry.lock          # Dependency lock file
└── pyproject.toml       # Project metadata and dependencies
```

## Installation and Execution

### Using Poetry

1. Install Poetry (if not already installed):
   ```
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. Install dependencies:
   ```
   poetry install
   ```

3. Activate the virtual environment:
   ```
   poetry shell
   ```

4. Run the application:
   ```
   uvicorn app.main:app --reload
   ```
   This will start the development server at [http://localhost:8000](http://localhost:8000).

### Using Docker Compose

1. Set up environment variables (copy from example if needed):
   ```
   cp .env-example .env
   ```

2. Start the containers:
   ```
   docker compose up
   ```
   This will start both the API service and the Qdrant vector database.

3. For development with auto-reload:
   ```
   docker compose up --build
   ```

### Using Docker (API only)

1. Build the Docker image:
   ```
   docker build -t faq-recommendations-backend .
   ```

2. Run the container:
   ```
   docker run -p 8000:8000 --env-file .env faq-recommendations-backend
   ```

The API will be available at [http://localhost:8000](http://localhost:8000) with interactive documentation at [http://localhost:8000/docs](http://localhost:8000/docs).
