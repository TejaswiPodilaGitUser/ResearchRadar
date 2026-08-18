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