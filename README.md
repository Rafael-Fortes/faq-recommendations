# FAQ Recommendations 🚀
Welcome to the FAQ-Recommendations repository! This application leverages semantic search, a technique that goes beyond keyword matching to understand the meaning and context of a user's query, in order to find FAQs that are truly relevant. 🔍

## Motivation 🎯
Users often seek answers to their questions about a particular service, product, etc. In such cases, they turn to a FAQ, where they can quickly find solutions without needing to interact with a support agent. FAQs are an essential tool for providing efficient and self-service support, empowering users to find solutions to their problems independently and at their own pace. By automating the process of finding answers, we reduce the burden on support teams and improve customer satisfaction. 😃

## Challenge 🤯
The challenge lies in analyzing a user's question and developing a system that can suggest relevant FAQs. This involves interpreting the meaning of the user's question and identifying FAQ questions that are semantically similar, even if the exact words don't match. 🤔

## How the challenge was solved 💡
We utilize transformer-based embeddings, such as those from the BERT or Sentence-BERT models, to transform FAQ questions and user questions into vector representations. This allows us to calculate the distance between these representations, enabling us to determine the similarity between the user's query and the FAQ questions. Embeddings capture the semantic relationships between words, and we use cosine similarity to measure the distance between these vectors, allowing the system to compare the meaning of questions rather than just their keywords. By using this approach, we can identify FAQ questions that are relevant to the user's query, even if they are phrased differently, thus ensuring that the user efficiently finds the information they seek. ✅

## Technologies Used 🛠️

### Backend
- **FastAPI**: Modern, high-performance web framework for building APIs with Python
- **Sentence Transformers**: Library for state-of-the-art sentence embeddings
- **Qdrant**: Vector database for efficient similarity search
- **Poetry**: Dependency management and packaging
- **Docker**: Containerization for easy deployment
- **Uvicorn**: ASGI server for running the FastAPI application

### Frontend
- **Next.js**: React framework for production-grade applications
- **React**: JavaScript library for building user interfaces
- **Tailwind CSS**: Utility-first CSS framework
- **Axios**: Promise-based HTTP client for making API requests
- **TypeScript**: Typed superset of JavaScript for improved developer experience
- **Docker**: Containerization for consistent environments

## Installation and Execution 🚀

### Prerequisites
- Docker and Docker Compose (for containerized setup)
- Node.js 18+ (for frontend development)
- Python 3.11+ (for backend development)

### Option 1: Using Docker Compose (Recommended)

This method launches both the frontend and backend services together:

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/faq-recommendations.git
   cd faq-recommendations
   ```

2. Set up environment variables:
   ```
   cp backend/.env-example backend/.env
   cp frontend/.env.example frontend/.env.local  # If needed
   ```

3. Start all services:
   ```
   docker compose up
   ```

4. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Option 2: Separate Development Setup

#### Backend Setup:
1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Install dependencies using Poetry:
   ```
   poetry install
   poetry shell
   ```

3. Start the backend server:
   ```
   uvicorn app.main:app --reload
   ```

#### Frontend Setup:
1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Start the development server:
   ```
   npm run dev
   ```

### Option 3: Individual Docker Containers

#### Backend:
```
cd backend
docker build -t faq-recommendations-backend .
docker run -p 8000:8000 --env-file .env faq-recommendations-backend
```

#### Frontend:
```
cd frontend
docker build -t faq-recommendations-frontend -f Dockerfile.dev .
docker run -p 3000:3000 -v $(pwd):/app -v /app/node_modules faq-recommendations-frontend
```

## Project Structure 📁

- **frontend/**: Next.js application with React UI components
- **backend/**: FastAPI application with vector search capabilities
- **docs/**: Additional documentation and resources

For more detailed information about each component, please refer to the README files in the respective directories.

## Acknowledgements 🙏
This challenge was proposed by Tech4humans at TechLab in 2023. I would like to thank Bruno Tanabe, with whom I collaborated to find a solution. 🤝