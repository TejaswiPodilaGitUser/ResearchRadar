# Backend Documentation — Research Radar
## 1. Overview

The Research Radar backend is a Python-based REST API built using FastAPI.

Its primary responsibilities are:

Ingesting research papers from OpenAlex
Persisting research data in PostgreSQL
Managing papers, authors, and topics
Providing REST APIs for paper discovery
Supporting keyword search and filtering
Supporting semantic similarity using embeddings and pgvector
Providing paper recommendations
Validating API requests
Handling application and database errors
Tracking API performance
Providing health and operational endpoints
Backend technology stack
Component	Technology
Language	Python 3.12
API Framework	FastAPI
ASGI Server	Uvicorn
ORM	SQLAlchemy
Validation	Pydantic
Database	PostgreSQL
Vector Database Extension	pgvector
Database Driver	psycopg2-binary
Migration Tool	Alembic
Data Source	OpenAlex
HTTP Client	HTTPX
Embedding Model	all-MiniLM-L6-v2
Embedding Library	Sentence Transformers
## 2. Backend Architecture

The backend follows a layered architecture.
```

                    ┌──────────────────────┐
                    │       Frontend       │
                    │   React / TypeScript │
                    └──────────┬───────────┘
                               │
                               │ HTTP / REST
                               ▼
                    ┌──────────────────────┐
                    │       FastAPI        │
                    │       Routers        │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │       Schemas        │
                    │     Validation       │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │       Services       │
                    │   Business Logic     │
                    └──────────┬───────────┘
                               │
                    ┌──────────┴───────────┐
                    ▼                      ▼
          ┌─────────────────┐    ┌──────────────────┐
          │   SQLAlchemy    │    │ Embedding Service│
          │      ORM        │    │ Sentence         │
          └────────┬────────┘    │ Transformers     │
                   │             └────────┬─────────┘
                   ▼                      │
          ┌─────────────────┐             │
          │   PostgreSQL    │◄────────────┘
          │    + pgvector   │
          └─────────────────┘
```
## 3. Project Structure

The backend is organized approximately as follows:
```
backend/
│
├── alembic/
│   ├── versions/
│   ├── env.py
│   ├── script.py.mako
│   └── README
│
├── alembic.ini
│
├── app/
│   │
│   ├── ai/
│   │   └── embedding_service.py
│   │
│   ├── api/
│   │   ├── papers.py
│   │   ├── authors.py
│   │   ├── topics.py
│   │   ├── recommendations.py
│   │   └── metrics.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── exceptions.py
│   │   ├── exception_handlers.py
│   │   ├── middleware.py
│   │   └── api_metrics.py
│   │
│   ├── database/
│   │   ├── base.py
│   │   └── database.py
│   │
│   ├── ingestion/
│   │   └── openalex_loader.py
│   │
│   ├── models/
│   │   ├── paper.py
│   │   ├── author.py
│   │   ├── topic.py
│   │   └── associations/
│   │       ├── paper_author.py
│   │       └── paper_topic.py
│   │
│   ├── schemas/
│   │   ├── paper_schema.py
│   │   ├── author_schema.py
│   │   └── ...
│   │
│   ├── services/
│   │   ├── paper_service.py
│   │   ├── author_service.py
│   │   ├── topic_service.py
│   │   └── recommendation_service.py
│   │
│   └── main.py
│
├── requirements.txt
├── Dockerfile
└── .env
```
The exact filenames may evolve as the project is refactored.

## 4. Application Entry Point

The FastAPI application starts from:
```
app/main.py
```
The application is responsible for:

Creating the FastAPI application
Registering API routers
Registering middleware
Registering exception handlers
Exposing health endpoints
Configuring application-level behavior

The application is started locally using:
```
uvicorn app.main:app --reload
```
Inside Docker:
```
uvicorn app.main:app --host 0.0.0.0 --port 8000
```
## 5. API Layer

The API layer contains FastAPI routers.

Its responsibility is to:

Receive HTTP requests
Validate request parameters
Call the appropriate service
Return response schemas
Avoid putting complex business logic directly inside route handlers

Typical flow:
```
HTTP Request
     │
     ▼
FastAPI Router
     │
     ▼
Validation
     │
     ▼
Service
     │
     ▼
Repository / SQLAlchemy
     │
     ▼
PostgreSQL
     │
     ▼
Response Schema
     │
     ▼
HTTP Response
```
## 6. Papers API

The main API is the paper discovery API.

List papers
```
GET /api/papers
```
Example:
```
GET /api/papers?page=1&size=20
```
The endpoint supports:

Pagination
Keyword search
Publication year
Topic
Author

Example:
```
GET /api/papers?keyword=machine%20learning
```
Example:
```
GET /api/papers?year=2024
```
Example:
```
GET /api/papers?topic=artificial%20intelligence
```
Example:
```
GET /api/papers?author=John
```
Multiple filters can be combined.

Example:
```
GET /api/papers?keyword=transformer&year=2024&page=1&size=20
```
## 7. Pagination

The API uses page-based pagination.

Example:

page = 1
size = 20

means:

First 20 records

The next page:

page = 2
size = 20

returns the next 20 records.

Pagination prevents the backend from returning the entire corpus for every request.

This becomes especially important as the number of papers grows.

## 8. Keyword Search

Keyword search operates against research-paper metadata.

The primary searchable fields are:

papers.title
papers.abstract

Conceptually:
```
User Query
     │
     ▼
Keyword Search
     │
     ├── title
     │
     └── abstract
     │
     ▼
Matching Papers
```
This provides traditional lexical search.

## 9. Paper Detail API
```
GET /api/papers/{paper_id}
```
Example:
```
GET /api/papers/10
```
The response includes paper metadata such as:

ID
OpenAlex ID
Title
Abstract
Publication year
Publication date
DOI
Citation count
Authors
Topics
Embedding-related information where appropriate

The endpoint is used by the frontend paper detail page.

## 10. Authors API

Author information is stored independently from papers.

Typical endpoints include:
```
GET /api/authors
```
and:
```
GET /api/authors/{author_id}
```
Authors are related to papers through the many-to-many relationship:
```
Paper
  │
  │
  ▼
paper_authors
  │
  ▼
Author
```
This avoids duplicating author records for every paper.

## 11. Topics API

Topics are also represented independently.

Typical endpoints include:
```
GET /api/topics
```
and:
```
GET /api/topics/{topic_id}
```
Paper/topic relationships are maintained through:

paper_topics
## 12. Database Layer

The backend uses SQLAlchemy for database access.

The database connection is defined in:
```
app/database/database.py
```
The application creates:

Engine
SessionLocal
get_db()

The engine connects to PostgreSQL using:
```
DATABASE_URL
```
## 13. Database Configuration

For local development, the database URL is typically:
```
postgresql://localhost:5432/research_radar
```
For Docker Compose:
```
postgresql://postgres:postgres@postgres:5432/research_radar
```
The important difference is the hostname.

Local
localhost
Docker
postgres

postgres is the Docker Compose service name.

The backend must not use localhost to connect to PostgreSQL when both services are running inside Docker.

## 14. Database Session

Database sessions are created using SQLAlchemy's sessionmaker.

The API obtains a database session through the dependency:

get_db()

Conceptually:
```
Request
   │
   ▼
get_db()
   │
   ▼
SessionLocal()
   │
   ▼
Service / Query
   │
   ▼
Database
   │
   ▼
Session closed
```
The session is closed after the request finishes.

## 15. SQLAlchemy Base

The declarative base is located in:
```
app/database/base.py
```
It contains the application's SQLAlchemy metadata.

Conceptually:
```
Base
 │
 ├── Paper
 ├── Author
 ├── Topic
 └── Association Tables
```
Alembic uses:
```
Base.metadata
```
to detect database schema changes during autogeneration.

## 16. Database Models

The core models are:

Paper
Author
Topic

Many-to-many association tables connect them.
```
                ┌─────────────┐
                │    Paper    │
                └──────┬──────┘
                       │
             ┌─────────┴─────────┐
             │                   │
             ▼                   ▼
      paper_authors        paper_topics
             │                   │
             ▼                   ▼
       ┌───────────┐       ┌───────────┐
       │  Author   │       │   Topic   │
       └───────────┘       └───────────┘
```
## 17. Paper Model

A paper contains research metadata such as:

id
openalex_id
title
abstract
publication_year
publication_date
doi
cited_by_count
embedding
created_at
updated_at

The embedding column stores the vector representation used for semantic search.

## 18. Author Model

The author model stores information such as:
```
id
name
orcid
```
The exact fields depend on the current schema.

An important design decision is that author identity is normalized instead of storing author information repeatedly in every paper.

## 19. Topic Model

Topics represent research areas associated with papers.

Examples:

Artificial Intelligence
Natural Language Processing
Machine Learning
Computer Vision

The relationship is many-to-many.

A paper can have multiple topics, and a topic can contain many papers.

## 20. Alembic Migrations

Database schema changes are managed using Alembic.

Migration configuration:
```
backend/alembic.ini
```
Migration environment:
```
backend/alembic/env.py
```
Migration scripts:
```
backend/alembic/versions/
```
The important principle is:

Database tables should be created through migrations rather than manually creating tables in PostgreSQL.

## 21. Running Migrations

From the backend directory:
```
cd backend
alembic upgrade head
```
Using Docker:
```
docker compose run --rm backend alembic upgrade head
```
The normal Docker startup command also runs migrations before starting FastAPI:
```
alembic upgrade head &&
uvicorn app.main:app --host 0.0.0.0 --port 8000
```
## 22. Migration Autogeneration

After changing SQLAlchemy models, a migration can be generated with:
```
alembic revision --autogenerate -m "description"
```
Then inspect the generated migration before applying it:
```
alembic upgrade head
```
Autogenerated migrations should always be reviewed manually.

This is particularly important for:

Foreign keys
Indexes
Vector columns
Renamed columns
Removed tables
Data migrations
## 23. OpenAlex Ingestion

Research data is retrieved from OpenAlex.

The ingestion implementation is located in:
```
app/ingestion/openalex_loader.py
```
The pipeline performs:
```
OpenAlex
   │
   ▼
Fetch Papers
   │
   ▼
Extract Metadata
   │
   ├── Paper
   ├── Authors
   └── Topics
   │
   ▼
Generate Embedding
   │
   ▼
PostgreSQL
```
## 24. Selected Research Topics

The ingestion pipeline currently uses:

Artificial Intelligence
Natural Language Processing

The OpenAlex endpoint is:
```
https://api.openalex.org
```
No API key is required for the assignment's basic ingestion workflow.

## 25. Ingestion Idempotency

The ingestion process is designed to be re-runnable.

The OpenAlex identifier is used to identify an existing paper.

Conceptually:
```
OpenAlex ID
     │
     ▼
Search database
     │
 ┌───┴────┐
 │        │
Exists   New
 │        │
Update   Insert
```
This prevents the same paper from being inserted repeatedly.

The same principle is used when resolving related entities.

## 26. Embedding Generation

Research-paper embeddings are generated using:
```
all-MiniLM-L6-v2
```
The embedding dimension is:
```
384
```
The text supplied to the embedding model is based primarily on:
```
Paper title
+
Paper abstract
```
Flow:
```
Title
  +
Abstract
   │
   ▼
Sentence Transformer
   │
   ▼
384-dimensional vector
   │
   ▼
pgvector
```
## 27. Semantic Similarity

The semantic-search capability uses PostgreSQL with pgvector.

Instead of matching only exact words, vector search compares the semantic representation of:

User query

against:

Paper embeddings

Conceptually:
```
Query
 │
 ▼
Embedding Model
 │
 ▼
Query Vector
 │
 ▼
pgvector
 │
 ▼
Similarity Calculation
 │
 ▼
Top Matching Papers
```
## 28. Why pgvector?

The dataset is relatively small for this assignment.

Using PostgreSQL + pgvector means we do not need a separate vector database.

Benefits:

Simple architecture
Fewer services
Easy local development
Transactional relational data and vectors in one database
SQLAlchemy integration
PostgreSQL ecosystem

For a much larger corpus, a dedicated vector-search infrastructure could be considered.

## 29. Search Architecture

The backend supports traditional and semantic discovery.
```
                  Search Request
                       │
             ┌─────────┴─────────┐
             │                   │
             ▼                   ▼
       Keyword Search       Semantic Search
             │                   │
             │             Embedding Model
             │                   │
             │                   ▼
             │              Query Vector
             │                   │
             └─────────┬─────────┘
                       ▼
                   Ranking
                       │
                       ▼
                  Paper Results
```
## 30. Recommendation Service

The recommendation service identifies papers related to a selected paper.

The general process is:
```
Selected Paper
      │
      ▼
Paper Embedding
      │
      ▼
Vector Similarity
      │
      ▼
Candidate Papers
      │
      ▼
Top Similar Papers
```
This provides a research-discovery experience beyond simple keyword matching.

## 31. Service Layer

Business logic is kept outside the API route wherever possible.

For example:
```
Router
   │
   ▼
Paper Service
   │
   ▼
Database Query
```
This provides separation between:

API layer

Responsible for:

HTTP
Request parameters
Response formatting
Service layer

Responsible for:

Business rules
Search logic
Recommendations
Data processing
Database layer

Responsible for:

SQLAlchemy sessions
Database persistence
Queries
## 32. Pydantic Schemas

Pydantic schemas define API input and output contracts.

They provide:

Type validation
Serialization
Consistent response structures
Request validation

For example, pagination parameters can be validated before the service executes the database query.

This prevents invalid requests from reaching the database.

## 33. Validation

The API validates inputs such as:

Page number
Page size
Search keyword
Year
Author filter
Topic filter
Resource IDs

Pagination should have an upper bound to prevent a client from requesting an unnecessarily large result set.

## 34. Exception Handling

The backend uses centralized exception handling.

Typical error categories include:

Validation Error
Resource Not Found
Database Error
Internal Server Error
Service Unavailable

A structured response is returned to clients.

Example:
```
{
  "error": {
    "code": "DATABASE_ERROR",
    "message": "A database error occurred"
  }
}
```
The implementation avoids exposing raw database internals to normal API consumers.

Detailed database exceptions remain available in backend logs for troubleshooting.

## 35. Database Error Handling

Database exceptions such as:
```
SQLAlchemyError
ProgrammingError
IntegrityError
```
are handled at the application boundary where appropriate.

For example, a database failure should result in a controlled API response instead of an unhandled stack trace being returned to the frontend.

## 36. Request Middleware

The backend includes request middleware for operational visibility.

The middleware can track:

Request ID
Request start time
Request duration
HTTP method
Path
Status code

The request ID is exposed using:

X-Request-ID

Example:
```
Client
   │
   │ GET /api/papers
   ▼
Middleware
   │
   ├── Generate Request ID
   ├── Start timer
   │
   ▼
FastAPI Router
   │
   ▼
Response
   │
   ├── Calculate duration
   └── Record metrics
   │
   ▼
Client
```
## 37. API Performance Metrics

The backend tracks API performance.

Current metrics include:

- Total requests
- Average response time
- P90 latency
- P95 latency
- P99 latency
- Errors
- Error rate

The current implementation uses an in-memory bounded collection.

This is sufficient for the assignment but has limitations.

Current limitations

Metrics:

Are lost when the application restarts
Are local to a single application instance
Are not historical
Are not shared between replicas

For production, the recommended architecture would be:
```
FastAPI
   │
   ▼
OpenTelemetry / Prometheus
   │
   ▼
Metrics Backend
   │
   ▼
Grafana
```
## 38. Health Check

The backend provides a health endpoint.

Example:
```
GET /health
```
Expected response:
```
{
  "status": "UP"
}
```
The health endpoint is useful for:

Docker
Kubernetes
Load balancers
Monitoring
Deployment verification

A production readiness improvement would be separating:
```
Liveness
Readiness
```
checks.

## 39. Configuration Management

Configuration is centralized in:
```
app/core/config.py
```
Environment variables are used for environment-specific settings.

Typical configuration:
```
DATABASE_URL
OPENALEX_BASE_URL
EMBEDDING_MODEL_NAME
EMBEDDING_DIMENSION
```
Local configuration:
```
postgresql://localhost:5432/research_radar
```
Docker configuration:
```
postgresql://postgres:postgres@postgres:5432/research_radar
```
The application should not hard-code environment-specific database URLs in business logic.

## 40. Docker Backend

The backend has its own Dockerfile.

The backend container runs:
```
Python 3.12
FastAPI
Uvicorn
SQLAlchemy
Alembic
psycopg2
pgvector
```
The backend is exposed on:
```
8000
```
Docker Compose starts the backend after PostgreSQL becomes healthy.

## 41. Docker Startup Flow

The Docker Compose startup sequence is:
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
Backend starts
        │
        ▼
Alembic migrations
        │
        ▼
FastAPI starts
        │
        ▼
Frontend starts
```
The database hostname from the backend container is:

postgres

not:

localhost
## 42. Running Backend with Docker

From the project root:
```
docker compose up --build
```
Or run the backend separately:
```
docker compose up --build backend
```
Check backend logs:
```
docker compose logs -f backend
```
Check PostgreSQL logs:
```
docker compose logs -f postgres
```
## 43. Running Alembic in Docker

Run migrations:
```
docker compose run --rm backend alembic upgrade head
```
Check migration state:
```
docker compose run --rm backend alembic current
```
Show migration history:
```
docker compose run --rm backend alembic history
```
Generate a migration:
```
docker compose run --rm backend \
alembic revision --autogenerate -m "description"
```
## 44. Running Ingestion in Docker

Once PostgreSQL and the backend environment are available:
```
docker compose run --rm backend \
python -m app.ingestion.openalex_loader
```
Monitor the output:

Fetched N papers
Processed N papers

The ingestion process commits the processed records to PostgreSQL.

## 45. Verify Database Data

Check tables:
```
docker compose exec postgres \
psql -U postgres -d research_radar -c "\dt"
```
Check papers:
```
docker compose exec postgres \
psql -U postgres -d research_radar \
-c "SELECT COUNT(*) FROM papers;"
```
Check authors:
```
docker compose exec postgres \
psql -U postgres -d research_radar \
-c "SELECT COUNT(*) FROM authors;"
```
Check topics:
```
docker compose exec postgres \
psql -U postgres -d research_radar \
-c "SELECT COUNT(*) FROM topics;"
```
## 46. API Documentation

FastAPI automatically provides Swagger UI.

Once the backend is running:
```
http://localhost:8000/docs
```
ReDoc:
```
http://localhost:8000/redoc
```
OpenAPI specification:
```
http://localhost:8000/openapi.json
```
Swagger is useful for manually testing:
```
Paper search
Filters
Pagination
Paper details
Recommendations
Metrics
Health checks
```
## 47. Testing Strategy

The API layer is the highest-value testing area.

Important test cases include:
```
Papers
GET /papers
GET /papers/{id}
```
Test:
```
Successful response
Pagination
Search
Year filter
Topic filter
Author filter
Empty result
Invalid parameters
Missing paper
Database
```
Test:
```
Database connection
Query behavior
Relationship loading
Error handling
```
Test:
```
404
422
Database errors
Invalid query parameters
```
## 48. Running Tests

If the project test suite is configured:
```
pytest
```
Verbose mode:
```
pytest -v
```
Run a specific test:
```
pytest tests/test_papers.py
```
Inside Docker:
```
docker compose run --rm backend pytest
```
## 49. Logging

The backend uses Python logging and Alembic logging.

Logs are particularly useful for:
```
Database failures
OpenAlex ingestion
API errors
Migration failures
Application startup
Request troubleshooting
```
In Docker:
```
docker compose logs -f backend
```
## 50. Common Docker Database Issues
Backend cannot connect to PostgreSQL

Incorrect:
```
DATABASE_URL=postgresql://localhost:5432/research_radar
```
Correct inside Docker:
```
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/research_radar
```
The Compose service name is:

postgres
## 51. papers does not exist

If the backend reports:

relation "papers" does not exist

check:
```
docker compose exec postgres \
psql -U postgres -d research_radar -c "\dt"
```
Then check Alembic:
```
docker compose run --rm backend alembic current
```
and:
```
docker compose run --rm backend alembic history
```
Apply migrations:
```
docker compose run --rm backend alembic upgrade head
```
## 52. vector does not exist

If PostgreSQL reports:

type "vector" does not exist

the pgvector extension has not been enabled in the database.

Check:
```
docker compose exec postgres \
psql -U postgres -d research_radar \
-c "SELECT extname FROM pg_extension;"
```
Enable pgvector:
```
docker compose exec postgres \
psql -U postgres -d research_radar \
-c "CREATE EXTENSION IF NOT EXISTS vector;"
```
Then retry:
```
docker compose run --rm backend alembic upgrade head
```
The Docker PostgreSQL image used by the project is:
```
pgvector/pgvector:pg16
```
## 53. Empty Database

A successful migration does not mean the database contains research data.

There are two separate operations:
```
Alembic
   │
   ▼
Creates database schema

and:

OpenAlex ingestion
   │
   ▼
Loads research data
```
Therefore the normal sequence is:
```
docker compose up --build
```
then:
```
docker compose run --rm backend \
python -m app.ingestion.openalex_loader
```
Then verify:
```
docker compose exec postgres \
psql -U postgres -d research_radar \
-c "SELECT COUNT(*) FROM papers;"
```
54. Idempotent Ingestion

The ingestion process should be safe to execute multiple times.

Example:
```
docker compose run --rm backend \
python -m app.ingestion.openalex_loader
```
Running it again should not blindly duplicate existing records.

The application uses OpenAlex identifiers and database relationships to identify existing records.

## 55. Backend Error Response Contract

The backend uses a consistent error structure.

Example:
```
{
  "error": {
    "code": "DATABASE_ERROR",
    "message": "A database error occurred"
  }
}
```
This gives the frontend a predictable contract.

The frontend can therefore display a user-friendly error without depending on raw Python or PostgreSQL error messages.

## 56. Production Considerations

The current implementation is designed for the assignment and a small research corpus.

For production scale, improvements could include:
```
Database
Connection pooling configuration
Read replicas
Query optimization
Additional indexes
Partitioning for very large datasets
Search
Full-text PostgreSQL search
Better hybrid-ranking algorithms
Dedicated search engine if required
Vector Search
Vector index tuning
HNSW / IVFFlat evaluation
Dedicated vector infrastructure at larger scale
Observability
Prometheus
Grafana
OpenTelemetry
Distributed tracing
Centralized logs
Platform
Kubernetes
Horizontal scaling
Redis caching
CI/CD
Cloud secrets management
Security
Authentication
Authorization
HTTPS
Rate limiting
Security headers
Secret management
```
## 57. Design Decisions
FastAPI

FastAPI was selected because it provides:

Strong type validation
Automatic OpenAPI documentation
High-performance async-capable APIs
Excellent Python ecosystem support
Simple dependency injection
SQLAlchemy

SQLAlchemy provides a mature ORM and database abstraction layer.

It also works well with:

PostgreSQL
Alembic
pgvector
Python type annotations
PostgreSQL

PostgreSQL was selected because the domain is highly relational.

For example:
```
Paper ↔ Author
Paper ↔ Topic
```
are naturally represented using relational many-to-many relationships.
```
pgvector
```
pgvector allows semantic search without introducing another database.

For this assignment's dataset size, this keeps deployment simple.

## 58. Backend Request Flow

A typical paper-search request follows:
```
Browser
   │
   │ GET /api/papers?keyword=AI
   ▼
FastAPI
   │
   ▼
Request Validation
   │
   ▼
Paper Router
   │
   ▼
Paper Service
   │
   ▼
SQLAlchemy Query
   │
   ▼
PostgreSQL
   │
   ▼
Result Mapping
   │
   ▼
Pydantic Response
   │
   ▼
JSON
   │
   ▼
Browser
```
## 59. Semantic Search Flow
```
Browser
   │
   │ Search Query
   ▼
FastAPI
   │
   ▼
Search Service
   │
   ▼
Embedding Service
   │
   ▼
384-dimensional Query Vector
   │
   ▼
PostgreSQL + pgvector
   │
   ▼
Similarity Ranking
   │
   ▼
Top Papers
   │
   ▼
API Response
```
60. Ingestion Flow
```
OpenAlex API
      │
      ▼
HTTPX Client
      │
      ▼
OpenAlex JSON
      │
      ▼
Normalize Data
      │
      ├──────────────┐
      ▼              ▼
   Authors         Topics
      │              │
      └──────┬───────┘
             ▼
           Paper
             │
             ▼
       Generate Embedding
             │
             ▼
        PostgreSQL
```
## 61. Operational Commands
Start everything
```
docker compose up --build
```
Start in background
```
docker compose up -d --build
```
Stop everything
```
docker compose down
```
Stop and remove database volume

Warning: this deletes PostgreSQL data.
```
docker compose down -v
```
View services
```
docker compose ps
```
Backend logs
```
docker compose logs -f backend
```
PostgreSQL logs
```
docker compose logs -f postgres
```
Restart backend
```
docker compose restart backend
```
## 62. Clean Database Reset

For a complete development reset:
```
docker compose down -v
```
Then:
```
docker compose up --build
```
The database will be recreated.

Run ingestion again:
```
docker compose run --rm backend \
python -m app.ingestion.openalex_loader
```
Verify:
```
docker compose exec postgres \
psql -U postgres -d research_radar \
-c "SELECT COUNT(*) FROM papers;"
```
This should only be used when deleting the existing development database is acceptable.

## 63. Backend Completion Checklist

The backend implementation should satisfy the following assignment requirements:
```
 Python backend
 FastAPI
 PostgreSQL
 SQLAlchemy
 Alembic migrations
 OpenAlex ingestion
 Idempotent ingestion
 Papers
 Authors
 Topics
 Many-to-many relationships
 Pagination
 Keyword search
 Year filtering
 Topic filtering
 Author filtering
 Paper detail API
 Embedding generation
 pgvector
 Similarity search
 Recommendation capability
 Validation
 Error handling
 Request tracking
 API metrics
 Docker support
```
Items marked complete should be re-verified before final submission from a clean checkout.

## 64. Recommended Evaluation Flow

An evaluator should be able to run:
```
git clone <repository-url>
cd ResearchRadar
docker compose up --build
```
Then:
```
docker compose run --rm backend \
python -m app.ingestion.openalex_loader
```
Verify:
```
curl http://localhost:8000/health
```
Then open:
```
http://localhost:5173
```
The complete flow is:
```
Clone Repository
      │
      ▼
docker compose up --build
      │
      ▼
PostgreSQL
      │
      ▼
Alembic Migration
      │
      ▼
FastAPI
      │
      ▼
OpenAlex Ingestion
      │
      ▼
Research Data
      │
      ▼
React Frontend
      │
      ▼
Search / Filter / Detail / AI Discovery
```
## 65. Summary

Research Radar's backend is designed around a simple principle:

Keep the architecture understandable while still demonstrating production-oriented engineering practices.

The backend separates:
```
API
 ↓
Validation
 ↓
Business Logic
 ↓
Persistence
 ↓
PostgreSQL
```
while the AI capability is isolated through:

Embedding Service

This allows the system to support semantic research discovery without unnecessarily introducing additional infrastructure.

The result is a backend that can be run locally, executed through Docker Compose, populated from OpenAlex, queried through REST APIs, and extended toward a production deployment.