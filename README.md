# Research Radar

Research Radar is a research-paper discovery platform that allows users to search, filter, explore, and semantically discover research papers using metadata and AI-powered vector search.

## Features

* Research paper ingestion from OpenAlex
* Paper, author, and topic management
* Pagination and filtering
* Keyword search
* Semantic search using embeddings
* Hybrid search using keyword + semantic similarity
* PostgreSQL database
* pgvector for vector similarity search
* REST APIs using FastAPI
* Pydantic response validation
* Centralized configuration
* Centralized exception handling
* Request logging/context
* API input validation and guardrails
* Health-check endpoint

---

## Architecture

```text
                    ┌──────────────────────┐
                    │      Client/UI       │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │       FastAPI        │
                    │       REST APIs      │
                    └──────────┬───────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
        Paper APIs        Search APIs      Recommendation
              │                │                │
              └────────────────┼────────────────┘
                               ▼
                    ┌──────────────────────┐
                    │      Services        │
                    │ Business Logic       │
                    └──────────┬───────────┘
                               │
                  ┌────────────┴────────────┐
                  │                         │
                  ▼                         ▼
          ┌───────────────┐        ┌──────────────────┐
          │ PostgreSQL    │        │ Embedding Service│
          │ + pgvector    │        │ Sentence         │
          │               │        │ Transformers     │
          └───────────────┘        └────────┬─────────┘
                                           │
                                           ▼
                                      Vector Search
```

---

## Technology Stack

* **Backend:** Python, FastAPI
* **ORM:** SQLAlchemy
* **Database:** PostgreSQL
* **Vector Database:** pgvector
* **Embeddings:** Sentence Transformers
* **Validation:** Pydantic
* **API Server:** Uvicorn
* **Data Source:** OpenAlex
* **Python:** 3.12

---

## Project Structure

```text
backend/
│
├── app/
│   ├── api/
│   │   ├── papers.py
│   │   ├── search.py
│   │   ├── authors.py
│   │   ├── topics.py
│   │   └── recommendations.py
│   │
│   ├── ai/
│   │   └── embedding_service.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── exceptions.py
│   │   ├── exception_handlers.py
│   │   └── middleware.py
│   │
│   ├── database/
│   │   └── database.py
│   │
│   ├── models/
│   │   ├── paper.py
│   │   ├── author.py
│   │   └── topic.py
│   │
│   ├── schemas/
│   │   └── paper_schema.py
│   │
│   ├── services/
│   │   ├── paper_service.py
│   │   └── search_service.py
│   │
│   └── main.py
│
├── scripts/
│   ├── update_embeddings.py
│   └── ...
│
├── .env
├── requirements.txt
└── README.md
```

### Main Components

| Component                    | Responsibility                                    |
| ---------------------------- | ------------------------------------------------- |
| `api/`                       | REST API endpoints                                |
| `services/`                  | Business logic and database operations            |
| `models/`                    | SQLAlchemy database models                        |
| `schemas/`                   | Pydantic API request/response models              |
| `ai/`                        | Embedding generation and AI-related functionality |
| `database/`                  | Database connection and session management        |
| `core/config.py`             | Application configuration                         |
| `core/exceptions.py`         | Custom application exceptions                     |
| `core/exception_handlers.py` | Centralized error responses                       |
| `core/middleware.py`         | Request context/logging                           |
| `scripts/`                   | Data and maintenance scripts                      |
| `main.py`                    | FastAPI application entry point                   |

---

## Current APIs

### Health

```http
GET /health
```

Returns application health status.

---

### Papers

```http
GET /papers
```

Supports:

* Pagination
* Keyword search
* Publication year
* Topic
* Author

Example:

```http
GET /papers?page=1&size=20
```

```http
GET /papers?keyword=artificial%20intelligence
```

```http
GET /papers?year=2024
```

```http
GET /papers?topic=machine%20learning
```

---

### Paper Details

```http
GET /papers/{paper_id}
```

Returns complete paper information including:

* Title
* Abstract
* Publication information
* DOI
* Authors
* Topics

Example:

```http
GET /papers/68
```

---

### Semantic Search

```http
GET /search
```

Uses Sentence Transformers to generate an embedding for the query and pgvector to perform cosine-similarity search.

Example:

```http
GET /search?q=artificial%20intelligence
```

---

### Hybrid Search

```http
GET /search/hybrid
```

Combines:

* Keyword matching
* Semantic vector similarity

Example:

```http
GET /search/hybrid?q=machine%20learning
```

---

### Authors

```http
GET /authors
GET /authors/{author_id}
```

Provides author listing and author details.

---

### Topics

```http
GET /topics
GET /topics/{topic_id}
```

Provides topic listing and topic details.

---

### Recommendations

```http
GET /recommendations
```

Provides research-paper recommendations based on the implemented recommendation logic.

---

## Error Handling

The application uses centralized exception handling.

Common HTTP responses include:

| Status | Meaning                      |
| ------ | ---------------------------- |
| `200`  | Successful request           |
| `400`  | Invalid request              |
| `404`  | Resource not found           |
| `422`  | Request validation failure   |
| `429`  | Rate limit exceeded          |
| `500`  | Internal server error        |
| `503`  | Service/database unavailable |

Application-specific errors use structured responses such as:

```json
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "Paper with id 68 not found"
  }
}
```

---

## Configuration

Application configuration is centralized in:

```text
app/core/config.py
```

Environment-specific values should be stored in `.env`.

Typical configuration includes:

```text
DATABASE_URL
APP_NAME
APP_VERSION

DEFAULT_PAGE
DEFAULT_PAGE_SIZE
MAX_PAGE_SIZE

MAX_KEYWORD_LENGTH
MAX_TOPIC_LENGTH
MAX_AUTHOR_LENGTH

MIN_PUBLICATION_YEAR
MAX_PUBLICATION_YEAR

EMBEDDING_MODEL_NAME
EMBEDDING_DIMENSION

DEFAULT_SEARCH_LIMIT
MAX_SEARCH_RESULTS
MIN_SEARCH_QUERY_LENGTH
MAX_SEARCH_QUERY_LENGTH
```

Secrets and environment-specific configuration should not be committed to Git.

---

## Embeddings

Research papers use vector embeddings for semantic search.

Current flow:

```text
Paper
  │
  ▼
Text
  │
  ▼
Sentence Transformer
  │
  ▼
Embedding Vector
  │
  ▼
PostgreSQL + pgvector
```

The query follows the same process:

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
pgvector Cosine Similarity
    │
    ▼
Relevant Papers
```

The embedding dimension must match the `pgvector` column definition.

---

## Database

The application uses PostgreSQL with pgvector.

Core entities:

```text
Paper
 ├── Authors
 └── Topics
```

A paper can have multiple authors and multiple topics.

The database currently contains research-paper data imported from OpenAlex.

---

## Completed

### Backend

* [x] FastAPI application
* [x] PostgreSQL integration
* [x] SQLAlchemy models
* [x] Paper model
* [x] Author model
* [x] Topic model
* [x] Pydantic schemas
* [x] Paper listing API
* [x] Paper details API
* [x] Author APIs
* [x] Topic APIs
* [x] Semantic search API
* [x] Hybrid search API
* [x] Recommendation API
* [x] Pagination
* [x] Filtering
* [x] Input validation
* [x] Configuration management
* [x] Centralized exception handling
* [x] Request middleware
* [x] Error codes
* [x] Embedding generation
* [x] pgvector integration
* [x] Embedding update script

---

## Current Status

The backend REST API and semantic-search foundation are implemented.

The database contains imported research papers and the embedding pipeline is available.

The next phase is focused on improving search/recommendation quality and completing the user-facing research discovery experience.

---

## Next Steps

### 1. Search Improvements

* Improve hybrid-search ranking
* Add configurable semantic/keyword weights
* Add search relevance scoring
* Improve filtering and sorting

### 2. Recommendations

* Implement similarity-based recommendations
* Recommend papers related to a selected paper
* Add configurable recommendation limits
* Add recommendation ranking

### 3. Data Pipeline

* Improve OpenAlex ingestion
* Add incremental synchronization
* Handle duplicate papers
* Handle updated papers
* Add ingestion validation

### 4. Frontend

Build the research discovery UI:

```text
Search
  ↓
Filters
  ↓
Paper Results
  ↓
Paper Details
  ↓
Related Papers
  ↓
Recommendations
```

### 5. Production Readiness

* Dockerization
* Database migrations
* Automated tests
* API integration tests
* CI/CD
* Structured logging
* Metrics
* Distributed tracing
* Rate limiting
* Security hardening

---

## Running the Backend

Activate the virtual environment:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the API:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

OpenAPI specification:

```text
http://127.0.0.1:8000/openapi.json
```

---

## Embedding Update

To generate/update embeddings:

```bash
python -m scripts.update_embeddings
```

The script identifies papers without embeddings and generates vectors using the configured Sentence Transformer model.

---

## API Documentation

Interactive API documentation is automatically provided by FastAPI through Swagger UI.

Use:

```text
/docs
```

for API testing and exploration.

---

## Development Principles

The backend follows a layered architecture:

```text
API
 ↓
Service
 ↓
Repository/Database
 ↓
PostgreSQL
```

Cross-cutting concerns such as configuration, exception handling, logging, validation, and middleware are kept outside the business logic.

The implementation also applies practical guardrails for:

* Input validation
* Pagination limits
* Search query length
* Result limits
* Error handling
* Database failures
* Unexpected exceptions
* Sensitive configuration
* API abuse/rate limiting

---

## License

This project is currently intended for educational and development purposes.
