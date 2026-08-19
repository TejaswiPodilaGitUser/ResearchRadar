# Research Radar — Architecture


## 1. Overview


Research Radar is a full-stack research discovery application that allows users to:


- Search research papers
- Filter papers by year, author, and topic
- View paper details
- Find similar papers using embeddings
- Monitor basic application/API metrics


The application uses a simple three-tier architecture.


```
text
                 ┌──────────────────────┐
                 │      React UI        │
                 │   TypeScript/Vite    │
                 └──────────┬───────────┘
                            │ HTTP/REST
                            ▼
                 ┌──────────────────────┐
                 │       FastAPI        │
                 │   REST API Layer     │
                 └──────────┬───────────┘
                            │
              ┌─────────────┴─────────────┐
              │                           │
              ▼                           ▼
      ┌─────────────────┐        ┌─────────────────┐
      │   PostgreSQL    │        │   Embedding     │
      │    + pgvector   │        │     Service     │
      └─────────────────┘        └─────────────────┘
```
## 2. Data Ingestion

Research papers are obtained from the OpenAlex API.
```
OpenAlex
   │
   ▼
Ingestion Service
   │
   ├── Papers
   ├── Authors
   ├── Topics
   └── Relationships
   │
   ▼
PostgreSQL
```
The ingestion process is designed to be re-runnable and avoids creating duplicate records.

## 3. Backend Architecture

The backend follows a layered structure:
```
API / Router
     │
     ▼
Service Layer
     │
     ▼
Database / Repository
     │
     ▼
PostgreSQL
API Layer
```
Responsible for:

HTTP endpoints
Request parameters
Response schemas
Validation
HTTP status codes
Service Layer

Contains application/business logic such as:

Paper search
Filtering
Recommendations
Author/topic operations
Embedding-based similarity
Database Layer

SQLAlchemy is used for database access.

Alembic is used for database schema migrations.

## 4. Database Model

The main entities are:
```
             ┌─────────────┐
             │    Paper    │
             └──────┬──────┘
                    │
          ┌─────────┴─────────┐
          │                   │
          ▼                   ▼
 ┌────────────────┐   ┌────────────────┐
 │     Author     │   │     Topic      │
 └────────────────┘   └────────────────┘
```
Many-to-many relationships are represented using:
```
paper_authors
paper_topics
```
Paper embeddings are stored in PostgreSQL using pgvector.

## 5. Search Architecture

Research Radar supports keyword and semantic search.

Keyword Search
```
User Query
    │
    ▼
FastAPI
    │
    ▼
PostgreSQL
    │
    ▼
Title / Abstract Matching
    │
    ▼
Results
Semantic Search
User Query
    │
    ▼
Sentence Transformer
    │
    ▼
Query Embedding
    │
    ▼
pgvector
    │
    ▼
Similarity Search
    │
    ▼
Similar Papers
```
This allows papers to be discovered even when the query does not use exactly the same terminology as the paper.

## 6. Frontend Architecture

The React application communicates with the backend through Axios.
```
React Page
    │
    ▼
API Client
    │
    ▼
FastAPI REST API
    │
    ▼
JSON Response
    │
    ▼
React State
    │
    ▼
UI
```
Main frontend areas include:

Search
Paper details
Recommendations
Metrics

Loading, empty, and error states are handled in the UI.

## 7. Docker Architecture

The application is containerized using Docker Compose.
```
┌───────────────────────────────────────────┐
│              Docker Compose               │
│                                           │
│  ┌────────────┐    ┌────────────┐         │
│  │  Frontend  │───▶│  Backend   │         │
│  │   Nginx    │    │  FastAPI   │         │
│  └────────────┘    └─────┬──────┘         │
│                          │                │
│                          ▼                │
│                   ┌────────────┐          │
│                   │ PostgreSQL │          │
│                   │ + pgvector │          │
│                   └────────────┘          │
└───────────────────────────────────────────┘
```
The backend waits for PostgreSQL to become healthy before starting migrations and the API.

## 8. Observability

The backend includes lightweight request monitoring.

Tracked information includes:

Request count
Response time
Error count
Error rate
P90 latency
P95 latency
P99 latency

Each request can also be associated with an X-Request-ID for troubleshooting.

For a production deployment, this could be extended with:

Prometheus
Grafana
OpenTelemetry
Centralized logging
## 9. Design Decisions
PostgreSQL + pgvector

A single PostgreSQL database keeps the architecture simple while supporting both relational data and vector similarity search.

Local Embeddings

all-MiniLM-L6-v2 provides semantic embeddings without requiring an external paid AI API.

FastAPI

FastAPI provides:

Strong request validation
Automatic OpenAPI documentation
Good async support
Lightweight REST API development
Docker Compose

Docker Compose provides a simple way to start the complete application and its dependencies consistently.

## 10. Future Architecture Improvements

For a larger production deployment, the architecture could evolve to include:
```
Load Balancer
      │
      ▼
Multiple FastAPI Instances
      │
 ┌────┴─────┐
 │          │
Redis    PostgreSQL
 │          │
Cache    + pgvector
```
Additional improvements could include:

Redis caching
Authentication/authorization
CI/CD
Prometheus monitoring
Distributed tracing
Cloud deployment
Dedicated vector database for very large datasets


This is a good **medium-sized architecture document** for the assignment—enough to demonstrate your design decisions without making the documentation unnecessarily large.