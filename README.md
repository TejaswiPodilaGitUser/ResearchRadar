

````markdown
# Research Radar

Research Radar is a full-stack research-paper discovery platform built to ingest, search, filter, explore, and semantically discover research papers.

The project was developed as a Full Stack / Platform Engineer assignment with a focus on:

- Clean API design
- Relational data modelling
- Search and filtering
- Semantic vector search
- Frontend usability
- API observability
- Error handling
- Production-oriented engineering practices

---

# Features

## Research Discovery

- Search research papers by keyword
- Search across paper titles and abstracts
- Filter by publication year
- Filter by author
- Filter by topic
- Paginated paper results
- Paper detail page
- Author and topic information

## AI / Semantic Search

- Sentence Transformer embeddings
- PostgreSQL + pgvector
- Semantic similarity search
- Hybrid keyword + semantic search
- Similarity-based recommendations

## Backend

- FastAPI REST APIs
- SQLAlchemy ORM
- Pydantic request/response validation
- Centralized configuration
- Centralized exception handling
- Request ID tracking
- Request timing
- API performance metrics
- Health-check endpoint
- Input validation and guardrails

## Frontend

- React
- TypeScript
- React Router
- Axios API client
- Search and filtering UI
- Paper detail UI
- Metrics dashboard
- Loading states
- Empty states
- API error states
- Responsive layout

## Observability

The application tracks API performance metrics including:

- Total requests
- Average response time
- Error count
- Error rate
- P90 latency
- P95 latency
- P99 latency

---

# Architecture

```text
                         ┌───────────────────────┐
                         │       React UI        │
                         │      TypeScript       │
                         └───────────┬───────────┘
                                     │
                                     │ REST / HTTP
                                     ▼
                         ┌───────────────────────┐
                         │       FastAPI         │
                         │       REST APIs       │
                         └───────────┬───────────┘
                                     │
                    ┌────────────────┼─────────────────┐
                    │                │                 │
                    ▼                ▼                 ▼
              Paper APIs       Search APIs       Metrics APIs
                    │                │                 │
                    └────────────────┼─────────────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │       Services        │
                         │    Business Logic     │
                         └───────────┬───────────┘
                                     │
                     ┌───────────────┴───────────────┐
                     │                               │
                     ▼                               ▼
             ┌─────────────────┐           ┌──────────────────┐
             │   PostgreSQL    │           │    Embedding     │
             │                 │           │     Service      │
             │    pgvector     │◄──────────│ Sentence         │
             │                 │           │ Transformers     │
             └─────────────────┘           └──────────────────┘
                     │
                     ▼
              Vector Similarity
                  Search
````

---

# Technology Stack

| Layer         | Technology            |
| ------------- | --------------------- |
| Frontend      | React + TypeScript    |
| Routing       | React Router          |
| HTTP Client   | Axios                 |
| Backend       | Python + FastAPI      |
| ORM           | SQLAlchemy            |
| Validation    | Pydantic              |
| Database      | PostgreSQL            |
| Vector Search | pgvector              |
| Embeddings    | Sentence Transformers |
| Data Source   | OpenAlex              |
| API Server    | Uvicorn               |
| Python        | 3.12                  |

---

# Data Source

## OpenAlex

The project uses the OpenAlex API as the research-paper data source.

OpenAlex was selected because:

* It is free to use
* No API key is required for basic usage
* It provides structured scholarly metadata
* It provides paper, author, topic, publication, and citation information
* It is suitable for reproducible ingestion

The ingestion pipeline retrieves papers for two research areas:

```text
Artificial Intelligence
Natural Language Processing
```

The ingestion process is designed to be:

* Re-runnable
* Idempotent
* Duplicate-aware
* Database-backed

Raw OpenAlex data dumps are not committed to the repository.

---

# Database Model

The core database entities are:

```text
                    ┌─────────────┐
                    │    Paper    │
                    └──────┬──────┘
                           │
                ┌──────────┴──────────┐
                │                     │
                ▼                     ▼
        ┌───────────────┐     ┌───────────────┐
        │    Authors    │     │    Topics     │
        └───────────────┘     └───────────────┘
```

Relationships:

```text
Paper ←→ Author
Paper ←→ Topic
```

Many-to-many relationships are represented using association tables.

Core entities include:

* Papers
* Authors
* Topics
* Paper Authors
* Paper Topics

Paper records also contain embeddings used by semantic search.

---

# Project Structure

```text
ResearchRadar/
│
├── backend/
│   │
│   ├── app/
│   │   │
│   │   ├── api/
│   │   │   ├── papers.py
│   │   │   ├── search.py
│   │   │   ├── authors.py
│   │   │   ├── topics.py
│   │   │   ├── recommendations.py
│   │   │   └── metrics.py
│   │   │
│   │   ├── ai/
│   │   │   └── embedding_service.py
│   │   │
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── exceptions.py
│   │   │   ├── exception_handlers.py
│   │   │   ├── middleware.py
│   │   │   └── api_metrics.py
│   │   │
│   │   ├── database/
│   │   │   └── database.py
│   │   │
│   │   ├── models/
│   │   │   ├── paper.py
│   │   │   ├── author.py
│   │   │   └── topic.py
│   │   │
│   │   ├── schemas/
│   │   │   └── paper_schema.py
│   │   │
│   │   ├── services/
│   │   │   ├── paper_service.py
│   │   │   └── search_service.py
│   │   │
│   │   └── main.py
│   │
│   ├── scripts/
│   │   ├── openalex_loader.py
│   │   └── update_embeddings.py
│   │
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   │
│   ├── src/
│   │   │
│   │   ├── api/
│   │   │   ├── axiosClient.ts
│   │   │   ├── papers.ts
│   │   │   ├── metrics.ts
│   │   │   └── apiMetrics.ts
│   │   │
│   │   ├── components/
│   │   │   ├── MetricsCards.tsx
│   │   │   └── ApiMetrics.tsx
│   │   │
│   │   ├── pages/
│   │   │   ├── SearchPage.tsx
│   │   │   ├── PaperDetailPage.tsx
│   │   │   └── Metrics.tsx
│   │   │
│   │   ├── styles/
│   │   │   ├── metrics.css
│   │   │   └── api-metrics.css
│   │   │
│   │   ├── app/
│   │   │   └── router.tsx
│   │   │
│   │   ├── App.tsx
│   │   └── main.tsx
│   │
│   └── package.json
│
├── README.md
└── docker-compose.yml
```

---

# Backend APIs

## Health

```http
GET /health
```

Example response:

```json
{
  "status": "UP"
}
```

---

## Papers

```http
GET /api/papers
```

Supports:

* Pagination
* Keyword search
* Publication year
* Topic
* Author

Example:

```http
GET /api/papers?page=1&size=20
```

```http
GET /api/papers?keyword=artificial%20intelligence
```

```http
GET /api/papers?year=2024
```

```http
GET /api/papers?topic=natural%20language%20processing
```

---

## Paper Details

```http
GET /api/papers/{paper_id}
```

Returns:

* Title
* Abstract
* Publication date
* Publication year
* DOI
* Authors
* Topics
* Citation metadata
* Other available paper metadata

Example:

```http
GET /api/papers/68
```

---

# Semantic Search

```http
GET /api/search
```

The search query is converted into an embedding using Sentence Transformers.

The resulting vector is compared against paper embeddings using pgvector.

```text
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
Cosine Similarity
     │
     ▼
Relevant Papers
```

Example:

```http
GET /api/search?q=machine%20learning
```

---

# Hybrid Search

```http
GET /api/search/hybrid
```

Hybrid search combines:

```text
Keyword relevance
        +
Semantic similarity
        ↓
Combined ranking
```

This provides better results for cases where an exact keyword match and semantic relevance need to be considered together.

Example:

```http
GET /api/search/hybrid?q=machine%20learning
```

---

# Recommendations

```http
GET /api/recommendations
```

The recommendation functionality uses the available paper metadata and semantic representation to identify relevant research papers.

The recommendation endpoint is designed to support similarity-based research discovery.

---

# Authors

```http
GET /api/authors
```

```http
GET /api/authors/{author_id}
```

Provides author listing and author details.

---

# Topics

```http
GET /api/topics
```

```http
GET /api/topics/{topic_id}
```

Provides topic listing and topic details.

---

# Metrics

Research corpus metrics:

```http
GET /api/metrics
```

Example:

```json
{
  "papers": 299,
  "authors": 1720,
  "topics": 741,
  "year_range": {
    "from": 2023,
    "to": 2025
  }
}
```

The frontend exposes these metrics through the Research Radar Metrics page.

---

# API Performance Metrics

```http
GET /api/metrics/performance
```

The application records API performance using request middleware.

Tracked metrics include:

```text
Requests
Average Response Time
Errors
Error Rate

P90 Latency
P95 Latency
P99 Latency
```

Example:

```json
{
  "requests": 22,
  "avg_response_ms": 56.68,
  "p90_latency_ms": 148.23,
  "p95_latency_ms": 297.01,
  "p99_latency_ms": 611.63,
  "errors": 0,
  "error_rate": 0.0
}
```

### Important limitation

The current implementation uses an in-memory metrics collector with a bounded sample window.

This is intentionally lightweight for the assignment.

For a production deployment, these metrics could be exported to:

* Prometheus
* Grafana
* CloudWatch
* OpenTelemetry

---

# Error Handling

The application uses centralized exception handling.

Common responses include:

| Status | Meaning                      |
| ------ | ---------------------------- |
| `200`  | Successful request           |
| `400`  | Invalid request              |
| `404`  | Resource not found           |
| `422`  | Request validation failure   |
| `429`  | Rate limit exceeded          |
| `500`  | Internal server error        |
| `503`  | Service/database unavailable |

Application errors use structured responses.

Example:

```json
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "Paper with id 68 not found"
  }
}
```

---

# Request Tracking

Each HTTP request receives a request ID.

```text
Client
  │
  │ X-Request-ID
  ▼
FastAPI Middleware
  │
  ├── Request ID
  ├── Start Time
  ├── Request Processing
  └── Response Time
          │
          ▼
       Response
```

The request ID is returned through:

```text
X-Request-ID
```

This makes request tracing and troubleshooting easier.

---

# Configuration

Application configuration is centralized in:

```text
backend/app/core/config.py
```

Environment-specific values are provided through `.env`.

Example:

```text
DATABASE_URL=postgresql://localhost:5432/research_radar

OPENALEX_BASE_URL=https://api.openalex.org

EMBEDDING_MODEL_NAME=all-MiniLM-L6-v2
EMBEDDING_DIMENSION=384
```

Pagination and validation limits are also configurable.

Secrets and environment-specific configuration should not be committed to Git.

---

# Embeddings

The current embedding model is:

```text
all-MiniLM-L6-v2
```

with:

```text
Dimension: 384
```

Embedding flow:

```text
Paper
  │
  ▼
Title + Abstract
  │
  ▼
Sentence Transformer
  │
  ▼
384-dimensional vector
  │
  ▼
PostgreSQL + pgvector
```

The same embedding model is used for query embeddings to ensure vector compatibility.

---

# Data Ingestion

The OpenAlex ingestion process:

```text
OpenAlex API
     │
     ▼
Fetch Papers
     │
     ▼
Validate / Normalize
     │
     ▼
Create / Update Authors
     │
     ▼
Create / Update Topics
     │
     ▼
Create / Update Papers
     │
     ▼
PostgreSQL
```

The ingestion process is designed to be idempotent.

Running the ingestion process multiple times should not create duplicate paper, author, or topic records.

---

# Current Dataset

The current local dataset contains approximately:

```text
Papers       299
Authors    1,720
Topics       741
```

Publication range:

```text
2023 – 2025
```

The exact count can change depending on the OpenAlex data returned during ingestion.

---

# Frontend

The frontend is implemented using:

```text
React
TypeScript
React Router
Axios
CSS
```

Main routes:

```text
/search
/papers/:paperId
/metrics
```

## Search Page

Provides:

* Search box
* Keyword search
* Filters
* Pagination
* Loading state
* Empty state
* Error state

---

## Paper Detail Page

Displays:

* Paper title
* Abstract
* Authors
* Publication year
* Topics
* DOI / metadata
* Research discovery functionality

---

## Metrics Page

Provides two categories of metrics.

### Research Corpus

```text
Papers
Authors
Topics
Publication Range
```

### API Performance

```text
Requests
Average Response
Errors
Error Rate

P90
P95
P99
```

---

# Database

PostgreSQL is used as the primary relational database.

pgvector is used for vector similarity search.

Core data model:

```text
papers
authors
topics
paper_authors
paper_topics
```

The paper embedding is stored alongside paper metadata.

---

# Database Migrations

Database schema changes should be managed using Alembic migrations.

Example:

```bash
alembic upgrade head
```

New schema changes should be introduced through migrations rather than manually creating database tables.

---

# Running Locally

## Prerequisites

Install:

* Python 3.12+
* Node.js
* PostgreSQL
* pgvector

---

## Backend

Navigate to the backend:

```bash
cd backend
```

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure `.env`:

```text
DATABASE_URL=postgresql://localhost:5432/research_radar
OPENALEX_BASE_URL=https://api.openalex.org
EMBEDDING_MODEL_NAME=all-MiniLM-L6-v2
EMBEDDING_DIMENSION=384
```

Run migrations:

```bash
alembic upgrade head
```

Start FastAPI:

```bash
uvicorn app.main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

OpenAPI:

```text
http://127.0.0.1:8000/openapi.json
```

---

# Data Ingestion

Run the OpenAlex ingestion script:

```bash
python -m app.ingestion.openalex_loader
```

The ingestion process can be safely re-run.

---

# Generate Embeddings

Run:

```bash
python -m scripts.update_embeddings
```

The script identifies papers without embeddings and generates vectors using the configured Sentence Transformer model.

---

# Frontend

Navigate to the frontend:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

The frontend will normally be available at:

```text
http://localhost:5173
```

---

# Docker

The target development experience is:

```bash
docker compose up
```

The complete application should start with:

```text
Frontend
   │
   ▼
FastAPI
   │
   ▼
PostgreSQL + pgvector
```

No raw dataset dumps are required in the repository.

---

# Testing

API-level tests are the primary testing focus because the backend contains the main business and data-access logic.

Important test areas include:

* Paper listing
* Pagination
* Search
* Filters
* Paper detail
* Not-found handling
* Validation errors
* Metrics endpoints
* Health endpoint

Run tests with:

```bash
pytest
```

---

# Engineering Decisions

## Why OpenAlex?

OpenAlex was selected because it provides a free scholarly metadata API without requiring an API key for this assignment.

It also provides useful relationships between papers, authors, topics, citations, and publication metadata.

---

## Why PostgreSQL?

PostgreSQL provides:

* Strong relational modelling
* Reliable transactions
* Flexible querying
* Mature indexing
* Excellent Python ecosystem support

It also supports pgvector, allowing relational and vector search capabilities to remain within the same database.

---

## Why pgvector?

Using pgvector avoids introducing a separate vector database for a relatively small corpus.

For this assignment, storing:

```text
Paper metadata
+
Embedding
```

in PostgreSQL keeps the architecture simple and easy to operate.

At larger scale, a dedicated vector-search infrastructure could be evaluated.

---

## Why Sentence Transformers?

A local embedding model avoids dependency on a paid external API and makes semantic search reproducible.

The selected model:

```text
all-MiniLM-L6-v2
```

provides a good balance between:

* Embedding quality
* Speed
* Model size
* Local execution

---

## Why Hybrid Search?

Keyword search works well for exact terminology.

Semantic search works better when the query and paper use different but related terminology.

Combining both approaches provides a more useful research discovery experience.

---

# Trade-offs

The implementation intentionally prioritizes simplicity because the assignment is time-boxed.

### In-memory API metrics

Current metrics are stored in application memory.

Advantages:

* Simple
* No additional infrastructure
* Easy to demonstrate

Limitations:

* Metrics reset when the application restarts
* Not suitable for multiple backend instances
* No historical metrics

A production implementation would use Prometheus/OpenTelemetry or a cloud monitoring platform.

### Local embeddings

Advantages:

* No external AI API dependency
* No API key
* Predictable cost
* Reproducible

Trade-off:

* CPU/memory usage
* Embedding generation can be slower than hosted services

### PostgreSQL + pgvector

Advantages:

* Simple architecture
* One database
* Easy local development

Trade-off:

For a very large corpus, a dedicated vector-search solution may provide better scalability.

---

# Security and Guardrails

The application includes practical API guardrails for:

* Request validation
* Query length
* Pagination limits
* Result limits
* Topic length
* Author filter length
* Publication-year validation
* Structured error handling
* Database exception handling
* Sensitive configuration through environment variables

Production deployment would additionally require:

* Authentication / authorization
* HTTPS
* Secret management
* WAF
* Rate limiting
* Security headers
* Audit logging

---

# Current Implementation Status

## Backend

* [x] FastAPI application
* [x] PostgreSQL integration
* [x] SQLAlchemy models
* [x] Paper model
* [x] Author model
* [x] Topic model
* [x] Many-to-many relationships
* [x] Pydantic schemas
* [x] Paper listing API
* [x] Paper detail API
* [x] Author APIs
* [x] Topic APIs
* [x] Search API
* [x] Hybrid search API
* [x] Recommendation API
* [x] Pagination
* [x] Filtering
* [x] Input validation
* [x] Configuration management
* [x] Centralized exception handling
* [x] Request middleware
* [x] Request ID
* [x] Request timing
* [x] API performance metrics
* [x] Embedding generation
* [x] pgvector integration
* [x] OpenAlex ingestion
* [x] Idempotent ingestion

## Frontend

* [x] React application
* [x] TypeScript
* [x] React Router
* [x] Axios API client
* [x] Search page
* [x] Paper detail page
* [x] Metrics page
* [x] Research corpus metrics
* [x] API performance metrics
* [x] P90/P95/P99 latency metrics
* [x] Loading states
* [x] Error states
* [x] Empty states
* [x] Responsive styling

## Remaining / Finalization

* [ ] Finalize AI feature on paper detail page
* [ ] Verify Alembic migrations
* [ ] Add/verify API tests
* [ ] Finalize Docker Compose
* [ ] Finalize README
* [ ] Clean Git history
* [ ] Final end-to-end verification
* [ ] Optional cloud deployment

---

# Future Improvements

With additional time, the following could be added:

### Search

* Better ranking algorithms
* Configurable hybrid-search weights
* Search result relevance scores
* Advanced filters
* Citation-based ranking

### AI

* Similar-paper explanations
* Abstract summarization
* Research trend detection
* Topic clustering

### Platform

* Redis caching
* Authentication
* Role-based access
* Prometheus metrics
* OpenTelemetry tracing
* CI/CD
* Automated security scanning
* Cloud deployment

---

# Project Goals

The primary goal of Research Radar is not to build a large production research platform.

The goal is to demonstrate a practical end-to-end engineering workflow:

```text
External Data
     ↓
Ingestion
     ↓
Data Modelling
     ↓
PostgreSQL
     ↓
REST APIs
     ↓
Search / Vector Search
     ↓
React UI
     ↓
Observability
```

The implementation intentionally favors a simple architecture that can be understood, run, tested, and extended easily.

---

# License

This project is currently intended for educational and development purposes.

```

### One important change before you commit this

Your README currently says some things are completed that **need to be verified against the actual repository**, especially:

- `Alembic`
- `Docker Compose`
- automated tests
- the final AI feature
- recommendation implementation

Don't claim those as `[x]` until they actually work from a fresh clone.

For the assignment, I'd also change the final status from **"next phase"** to **"implementation status"**, because your project has progressed considerably beyond the original README.
```
