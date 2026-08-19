

https://github.com/user-attachments/assets/e9ca082f-23d1-4883-939d-308d6dd193d7





<img width="1552" height="862" alt="image" src="https://github.com/user-attachments/assets/423da1c5-9ca1-4df7-89e0-78032be683b3" />


<img width="1538" height="838" alt="image" src="https://github.com/user-attachments/assets/3bd084b0-4da4-45d4-8c50-3d231e2984f0" />




<img width="1420" height="860" alt="image" src="https://github.com/user-attachments/assets/3eba6c47-b94d-42de-8fed-7ed5126d4eb1" />


<img width="1371" height="814" alt="image" src="https://github.com/user-attachments/assets/2f7bd79e-d910-406f-afae-686932f4e893" />


<img width="1397" height="727" alt="image" src="https://github.com/user-attachments/assets/f416b118-4751-4250-aedc-bc6c861f796f" />


<img width="1499" height="786" alt="image" src="https://github.com/user-attachments/assets/8628168c-76bb-45fb-9dfc-7b68088a4498" />




# Research Radar

Research Radar is a full-stack research discovery platform for searching, filtering, exploring, and finding similar research papers.

The application demonstrates an end-to-end engineering workflow:

OpenAlex → Data Ingestion → PostgreSQL + pgvector → FastAPI → React → AI-powered Research Discovery

---

## 1. Project Overview

Research Radar allows users to:

- Search research papers
- Search by title and abstract
- Filter by publication year
- Filter by author
- Filter by topic
- Paginate search results
- View complete paper details
- Find semantically similar papers
- Use vector embeddings for AI-powered research discovery
- View application and API performance metrics
- Handle loading, empty, validation, and API error states

The project uses OpenAlex as the research data source.

### Why OpenAlex?

OpenAlex was selected because:

- It is free
- No API key is required for the assignment
- It provides scholarly metadata
- It provides paper, author, topic, publication, and citation information
- It is suitable for reproducible ingestion
- It does not require committing raw research data into the repository

---

# 2. Technology Stack

## Backend

- Python 3.12
- FastAPI
- SQLAlchemy
- Pydantic
- Alembic
- Uvicorn
- PostgreSQL
- pgvector

## AI / Search

- Sentence Transformers
- all-MiniLM-L6-v2
- 384-dimensional embeddings
- PostgreSQL pgvector
- Cosine similarity
- Semantic search
- Hybrid search

## Frontend

- React
- TypeScript
- Vite
- React Router
- Axios
- CSS


## Infrastructure

- Docker
- Docker Compose
- PostgreSQL + pgvector
- Nginx

---

# 3. Architecture

```text
                    ┌─────────────────────┐
                    │    React Frontend   │
                    │    TypeScript       │
                    └──────────┬──────────┘
                               │
                           HTTP / REST
                               │
                               ▼
                    ┌─────────────────────┐
                    │       FastAPI       │
                    │     REST Backend     │
                    └──────────┬──────────┘
                               │
                ┌──────────────┼──────────────┐
                │              │              │
                ▼              ▼              ▼
          Paper APIs      Search APIs    Metrics APIs
                │              │
                │              ▼
                │       Embedding Service
                │              │
                └───────┬──────┘
                        ▼
               PostgreSQL + pgvector
                        │
                        ▼
                 Similarity Search

```

# 4. Data Flow
```
OpenAlex API
     │
     ▼
Ingestion Service
     │
     ├── Papers
     ├── Authors
     ├── Topics
     └── Embeddings
     │
     ▼
PostgreSQL + pgvector
     │
     ▼
FastAPI REST API
     │
     ▼
React Frontend
```
# 5. Project Structure
```
ResearchRadar/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── ai/
│   │   ├── core/
│   │   ├── database/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── ingestion/
│   │   └── main.py
│   │
│   ├── alembic/
│   │   ├── versions/
│   │   └── env.py
│   │
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env
│
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── styles/
│   │   ├── app/
│   │   └── main.tsx
│   │
│   ├── package.json
│   ├── Dockerfile
│   └── nginx.conf
│
├── documentation/
│   ├── BACKEND.md
│   ├── FRONTEND.md
│   ├── DOCKER.md
│   ├── ARCHITECTURE.md
│   ├── DATABASE.md
│   ├── TESTING.md
│   ├── API.md
│   └── AI_SEARCH.md
│
├── docker-compose.yml
└── README.md
```
# 6. Database

The main database tables are:
```
papers
authors
topics
paper_authors
paper_topics

Relationships:

Paper ←→ Author
Paper ←→ Topic
```
The papers table also contains the embedding used for semantic similarity.

Database schema changes are managed using Alembic.

No application tables are manually created.

# 7. AI Feature

The selected AI feature is:

Find Similar Papers

The paper title and abstract are converted into an embedding using:

all-MiniLM-L6-v2

Embedding dimension:

384

Flow:
```
Paper
  │
  ▼
Title + Abstract
  │
  ▼
Sentence Transformer
  │
  ▼
384-dimensional Embedding
  │
  ▼
PostgreSQL + pgvector
  │
  ▼
Cosine Similarity
  │
  ▼
Similar Papers
```
This approach was selected because the assignment requires one AI feature and the semantic similarity feature provides useful research discovery functionality without requiring a paid external LLM API.

# 8. Backend APIs
```
Health
GET /health
Papers
GET /papers
GET /papers/{id}
```
Supports:

Pagination
Keyword search
Year filtering
Topic filtering
Author filtering

Example:
```
GET /papers?page=1&size=20
GET /papers?keyword=machine%20learning
Authors
GET /authors
GET /authors/{id}
Topics
GET /topics
GET /topics/{id}
Search
GET /search
Recommendations
GET /recommendations
Metrics
GET /metrics
GET /metrics/performance
```
# 9. Swagger API Documentation

After starting the backend:
```
http://localhost:8000/docs
```
OpenAPI specification:
```
http://localhost:8000/openapi.json
```
# 10. Docker - Recommended Way to Run

Docker Compose is the recommended way to run the complete application.

The complete stack contains:
```
PostgreSQL + pgvector
        │
        ▼
     FastAPI
        │
        ▼
      Nginx
        │
        ▼
      React
```
# 11. Prerequisites

Install:

Docker Desktop
Git

Docker Desktop includes Docker Compose.

Verify:
```
docker --version
docker compose version
```
# 12. Clone Repository
```
git clone <repository-url>

cd ResearchRadar
```
# 13. Start Application

Recommended command:
```
docker compose up --build
```
Or run in background:
```
docker compose up -d --build
```
Check containers:
```
docker compose ps
```
Expected services:
```
research-radar-postgres
research-radar-backend
research-radar-frontend
```
# 14. Application URLs

Frontend:
```
http://localhost:5173
```
Backend:
```
http://localhost:8000
```
Swagger:
```
http://localhost:8000/docs
```
Health:
```
http://localhost:8000/health
```
# 15. Docker Startup Flow

The backend automatically executes:
```
alembic upgrade head
```
before starting FastAPI.

Startup flow:
```
docker compose up
       │
       ▼
PostgreSQL starts
       │
       ▼
PostgreSQL health check
       │
       ▼
Alembic migrations
       │
       ▼
FastAPI starts
       │
       ▼
Nginx starts
       │
       ▼
React application available
```

Therefore, normally only this command is required:
```
docker compose up --build
```
# 16. Load Research Data

After the containers are running:

docker compose exec backend python -m app.ingestion.openalex_loader

The ingestion process:

Calls OpenAlex
Fetches research papers
Creates or updates papers
Creates or updates authors
Creates or updates topics
Generates embeddings
Stores data in PostgreSQL

The ingestion process is designed to be re-runnable and idempotent.

# 17. Verify Database

Check tables:
```
docker compose exec postgres psql -U postgres -d research_radar -c "\dt"
```
Check papers:
```
docker compose exec postgres psql -U postgres -d research_radar -c "SELECT COUNT(*) FROM papers;"
```
Check authors:
```
docker compose exec postgres psql -U postgres -d research_radar -c "SELECT COUNT(*) FROM authors;"
```
Check topics:
```
docker compose exec postgres psql -U postgres -d research_radar -c "SELECT COUNT(*) FROM topics;"
```
Check embeddings:
```
docker compose exec postgres psql -U postgres -d research_radar -c "SELECT COUNT(*) FROM papers WHERE embedding IS NOT NULL;"
```
# 18. Useful Docker Commands
```
Start
docker compose up
Build and Start
docker compose up --build
Start in Background
docker compose up -d
Stop
docker compose down
Check Status
docker compose ps
View All Logs
docker compose logs
Backend Logs
docker compose logs backend
Follow Backend Logs
docker compose logs -f backend
Frontend Logs
docker compose logs frontend
PostgreSQL Logs
docker compose logs postgres
Restart Backend
docker compose restart backend
Restart Everything
docker compose restart
```
# 19. Clean Docker Reset

If the database or containers become inconsistent:
```
docker compose down -v --remove-orphans
```
Then:
```
docker compose up --build
```
Run ingestion again:
```
docker compose exec backend python -m app.ingestion.openalex_loader
```
WARNING:
```
docker compose down -v
```
deletes the PostgreSQL Docker volume and therefore deletes the local database data.

Use this only when a clean database is required.

# 20. Database Migration Commands

Check migration status:
```
docker compose exec backend alembic current
```
View migration history:
```
docker compose exec backend alembic history
```
Apply migrations:
```
docker compose exec backend alembic upgrade head
```
Alembic migrations are automatically executed during normal Docker startup.

# 21. Local Development Without Docker

Docker is recommended, but the application can also be run locally.

Backend
```
cd backend
```
Create virtual environment:
```
python -m venv venv
```
Activate:
```
source venv/bin/activate
```
Install dependencies:
```
pip install -r requirements.txt
```
Configure database:
```
DATABASE_URL=postgresql://localhost:5432/research_radar
```
Run migrations:

alembic upgrade head

Start backend:
```
uvicorn app.main:app --reload
```
Backend:
```
http://localhost:8000
```
Swagger:
```
http://localhost:8000/docs
```
# 22. Local Data Ingestion

With the backend environment activated:
```
python -m app.ingestion.openalex_loader
```
Verify:
```
psql -U postgres -d research_radar
```
Then:
```
SELECT COUNT(*) FROM papers;
```
# 23. Frontend Local Development
```
cd frontend
```
Install dependencies:
```
npm install
```
Configure:
```
VITE_API_BASE_URL=http://localhost:8000
```
Start:
```
npm run dev
```
Frontend:
```
http://localhost:5173
```
# 24. Frontend Docker Configuration

The frontend uses Vite environment variables during the Docker build.

The Docker Compose configuration should contain:
```
frontend:
  build:
    context: ./frontend
    dockerfile: Dockerfile
    args:
      VITE_API_BASE_URL: http://localhost:8000
```
The frontend Dockerfile receives this build argument and makes it available to Vite.

After changing the API URL, rebuild:

docker compose build --no-cache frontend

Then:
```
docker compose up -d
```
# 25. Troubleshooting
Frontend Error
VITE_API_BASE_URL is not configured

Verify docker-compose.yml:

args:
  VITE_API_BASE_URL: http://localhost:8000

Rebuild:
```
docker compose build --no-cache frontend
```
Start:
```
docker compose up -d
```
# 26. Backend Cannot Connect to PostgreSQL

Check:
```
docker compose ps
```
PostgreSQL should show:

healthy

Check logs:

docker compose logs postgres

Test database:

docker compose exec postgres psql -U postgres -d research_radar -c "SELECT 1;"

Inside Docker, the database hostname is:

postgres

Therefore the backend database URL should be:
```
postgresql://postgres:postgres@postgres:5432/research_radar
```
# 27. PostgreSQL Vector Error

If you see:

type "vector" does not exist

Verify pgvector:
```
docker compose exec postgres psql -U postgres -d research_radar -c "\dx"
```
If required:
```
docker compose exec postgres psql -U postgres -d research_radar -c "CREATE EXTENSION IF NOT EXISTS vector;"
```
Then:
```
docker compose exec backend alembic upgrade head
```
# 28. Alembic Migration Error

Check:
```
docker compose exec backend alembic current
```
Check:
```
docker compose exec backend alembic history
```
Run:
```
docker compose exec backend alembic upgrade head
```
If this is only a local development database and the database can be recreated:
```
docker compose down -v
```
Then:
```
docker compose up --build
```
# 29. Empty Database

If tables exist but contain no data:
```
docker compose exec postgres psql -U postgres -d research_radar -c "SELECT COUNT(*) FROM papers;"
```
Run ingestion:
```
docker compose exec backend python -m app.ingestion.openalex_loader
```
Then verify:
```
docker compose exec postgres psql -U postgres -d research_radar -c "SELECT COUNT(*) FROM papers;"
```
# 30. Ingestion Failure

View backend logs:
```
docker compose logs -f backend
```
Run manually:
```
docker compose exec backend python -m app.ingestion.openalex_loader
```
Check OpenAlex connectivity:
```
docker compose exec backend python -c "import httpx; print(httpx.get('https://api.openalex.org/works?per-page=1').status_code)"
```
Expected:
```
200
```
# 31. Frontend Cannot Reach Backend

Verify backend:
```
curl http://localhost:8000/health
```

Expected:
```
{
  "status": "UP"
}
```
The browser-facing API URL should be:
```
http://localhost:8000
```
Do not configure the frontend browser to use:
```
http://backend:8000
```
backend is only a Docker-internal hostname.

##  Port Already in Use

Check:
```
lsof -i :5173
lsof -i :8000
lsof -i :5432
```
Stop the conflicting process or change the Docker port mapping.

# 32. Testing

Run backend tests:

docker compose exec backend pytest

Or locally:
```
cd backend
pytest
```
Important test areas:

Health endpoint
Paper API
Pagination
Search
Filters
Paper details
Validation
Error handling
Metrics

See:
```
documentation/TESTING.md
```

# 33. Testing individual files
From your backend/ directory, you can run individual pytest files like this:

1. Run one test file
```
pytest -v tests/test_papers.py
```

You can run:
```
pytest -v tests/test_papers.py
pytest -v tests/test_authors.py
pytest -v tests/test_topics.py
pytest -v tests/test_recommendations.py
```
Recommended while debugging:
```
pytest -v -s tests/test_papers.py
```
# 34. API Documentation

Detailed API documentation:
```
documentation/API.md
```
Backend Swagger:
```
http://localhost:8000/docs
```
Main APIs:
```
GET /health


GET /papers
GET /papers/{id}


GET /authors
GET /authors/{id}


GET /topics
GET /topics/{id}


GET /search


GET /recommendations


GET /metrics
GET /metrics/performance
# 35. Observability
```
The backend tracks:

Total requests
Average response time
P90 latency
P95 latency
P99 latency
Error count
Error rate

Each request also receives:

X-Request-ID

This provides basic request tracing and troubleshooting.

For production, this can be extended with:

Prometheus
Grafana
OpenTelemetry
CloudWatch
# 36. Error Handling

The application handles:

Invalid requests
Validation errors
Missing resources
Database errors
API errors
Empty search results
Service failures

The frontend provides:

Loading states
Empty states
Error states
Retry/navigation options
# 37. Configuration

Configuration is environment-based.

Typical values include:
```
DATABASE_URL
OPENALEX_BASE_URL
EMBEDDING_MODEL_NAME
EMBEDDING_DIMENSION
```
Example:
```
DATABASE_URL=postgresql://localhost:5432/research_radar
OPENALEX_BASE_URL=https://api.openalex.org
EMBEDDING_MODEL_NAME=all-MiniLM-L6-v2
EMBEDDING_DIMENSION=384
```
Secrets must not be committed to Git.

# 38. Production Deployment

Docker Compose is intended for local development and evaluation.

A production deployment should use:
```
Internet
   │
   ▼
Load Balancer
   │
   ├───────────────┐
   ▼               ▼
Frontend         Backend
Nginx            FastAPI
                    │
                    ▼
            Managed PostgreSQL
                + pgvector
```

Recommended production components:
```
HTTPS
Load balancer
Managed PostgreSQL
Private database networking
Container registry
Secret manager
CI/CD
Centralized logging
Monitoring
Health checks
Autoscaling
```
# 39. Production Security

Production should use:

HTTPS
Authentication
Authorization
Secret management
Private database
Database encryption
Security headers
Rate limiting
Audit logging
Dependency scanning

The PostgreSQL port should normally not be publicly exposed in production.

The following is useful for local development:
```
ports:
  - "5432:5432"
```
but should generally be removed or restricted in production.

# 40. Production Configuration Principles

Do not hard-code:

Passwords
API keys
Secret keys
Cloud credentials

Use:

Environment variables
Docker secrets
Cloud secret managers

The production database should be managed separately from the application containers.

# 41. Design Decisions
OpenAlex

OpenAlex provides free scholarly metadata without requiring an API key for this assignment.

PostgreSQL

PostgreSQL provides:

Relational modelling
Transactions
Indexing
Mature ecosystem
pgvector support
pgvector

pgvector was selected instead of a separate vector database because the corpus is relatively small and PostgreSQL can handle both relational and vector data.

Sentence Transformers

all-MiniLM-L6-v2 provides a practical balance between:

Embedding quality
Runtime
Model size
Local execution
FastAPI

FastAPI provides:

Automatic OpenAPI documentation
Validation
Type hints
Lightweight REST API development
React + TypeScript

React provides a flexible UI architecture and TypeScript improves frontend maintainability and type safety.

# 42. Trade-offs

The project is time-boxed and intentionally avoids unnecessary infrastructure.

In-memory API Metrics

Advantages:

Simple
No additional infrastructure
Easy to demonstrate

Limitations:

Metrics reset when the application restarts
Not suitable for distributed instances
No historical metrics

Production improvement:

Prometheus + Grafana
Local Embeddings

Advantages:

No external API key
No API cost
Reproducible

Trade-off:

CPU and memory usage
Embedding generation can take time
PostgreSQL + pgvector

Advantages:

Simple architecture
One database
Easy local development

Trade-off:

A very large corpus may require dedicated vector-search infrastructure.

# 43. Current Implementation Status
```
Backend
 FastAPI
 PostgreSQL
 SQLAlchemy
 Pydantic
 Alembic
 Papers
 Authors
 Topics
 Many-to-many relationships
 Pagination
 Search
 Filters
 Paper details
 OpenAlex ingestion
 Idempotent ingestion
 Embeddings
 pgvector
 Similarity search
 Error handling
 Request IDs
 API metrics
 Health checks
Frontend
 React
 TypeScript
 Vite
 React Router
 Axios
 Search page
 Filters
 Pagination
 Paper detail page
 Similar papers
 Metrics page
 Loading states
 Empty states
 Error states
 Responsive UI
Infrastructure
 Docker
 Docker Compose
 PostgreSQL container
 pgvector
 Backend container
 Frontend container
 Nginx
 Automatic migrations
 ```
# 44. Known Limitations

This is a time-boxed engineering assignment and not a complete production SaaS platform.

Current limitations include:

In-memory API metrics
No authentication
No distributed tracing
No Redis caching
No CI/CD pipeline
Local embedding model
Single PostgreSQL instance in Docker Compose
No Kubernetes deployment
No cloud deployment by default

These are natural next steps for a production deployment.

# 45. Future Improvements
Platform
Kubernetes deployment
CI/CD
Horizontal scaling
Redis caching
Authentication
Authorization
Managed PostgreSQL
Observability
Prometheus
Grafana
OpenTelemetry
Distributed tracing
Centralized logging
Search
PostgreSQL full-text search
Improved hybrid ranking
Citation-based ranking
Advanced filters
Search relevance scoring
AI
Better embedding models
LLM-powered summaries
Explainable recommendations
Research trend detection
Topic clustering
# 46. Final Clean Start

If you need to completely recreate the local environment:
```
docker compose down -v --remove-orphans
```
Build:
```
docker compose build --no-cache
```
Start:
```
docker compose up -d
```
Check:
```
docker compose ps
```
Run ingestion:
```
docker compose exec backend python -m app.ingestion.openalex_loader
```
Check data:
```
docker compose exec postgres psql -U postgres -d research_radar -c "SELECT COUNT(*) FROM papers;"
```
Open:
```
http://localhost:5173
```
# 47. Recommended Reviewer Flow

A reviewer can run the complete application using:
```
git clone <repository-url>
cd ResearchRadar
docker compose up --build
```
Then:
```
http://localhost:5173
```
If the database is initially empty:

docker compose exec backend python -m app.ingestion.openalex_loader

Then refresh the frontend.

The reviewer can verify:

Application startup
Search
Filters
Pagination
Paper details
Similar-paper AI feature
API documentation
Database
Error handling
API metrics
# 48. Documentation

Additional project documentation is available under:

documentation/

Files:

BACKEND.md
FRONTEND.md
DOCKER.md
ARCHITECTURE.md
DATABASE.md
TESTING.md
API.md
AI_SEARCH.md
# 49. Final Summary

Research Radar demonstrates an end-to-end full-stack research discovery platform:
```

                    OpenAlex
                       │
                       ▼
                Data Ingestion
                       │
                       ▼
              PostgreSQL + pgvector
                       │
                       ▼
                    FastAPI
                       │
             ┌─────────┴─────────┐
             │                   │
             ▼                   ▼
        REST Search        AI Similarity
             │                   │
             └─────────┬─────────┘
                       ▼
                React Frontend
                       │
                       ▼
              Research Discovery
```
The application is designed to be:

Easy to run
Dockerized
Re-runnable
Idempotent
Testable
Maintainable
Observable
Extensible toward production
Quick Start
```
git clone <repository-url>
cd ResearchRadar
docker compose up --build
```
Open:
```
http://localhost:5173
```
Backend:
```
http://localhost:8000
```
Swagger:
```
http://localhost:8000/docs
```
If the database is empty:
```
docker compose exec backend python -m app.ingestion.openalex_loader
```
# 50. License

This project was developed as an assignment and is intended for evaluation and development purposes.                 
