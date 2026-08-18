DATABASE.md
# Research Radar — Database


## 1. Overview


Research Radar uses **PostgreSQL** as the primary database.


The database stores:


- Research papers
- Authors
- Topics
- Paper-author relationships
- Paper-topic relationships
- Paper embeddings


`pgvector` is used to store embeddings and perform similarity searches.


---


## 2. Database Technology


| Component | Technology |
|---|---|
| Database | PostgreSQL 16 |
| Vector Extension | pgvector |
| ORM | SQLAlchemy |
| Migration Tool | Alembic |
| Driver | psycopg2 |
| Embedding Dimension | 384 |


---


## 3. Entity Model


The main entities are:


```text
              ┌──────────────┐
              │    Papers    │
              └──────┬───────┘
                     │
          ┌──────────┴──────────┐
          │                     │
          ▼                     ▼
 ┌────────────────┐     ┌────────────────┐
 │    Authors     │     │     Topics     │
 └────────────────┘     └────────────────┘

Because a paper can have multiple authors and topics, many-to-many association tables are used.

papers
   │
   ├── paper_authors ── authors
   │
   └── paper_topics ─── topics
4. Papers Table

The papers table contains the main research-paper metadata.

Important fields:

Column	Purpose
id	Primary key
openalex_id	Unique OpenAlex identifier
title	Paper title
abstract	Paper abstract
publication_year	Publication year
publication_date	Publication date
doi	DOI
cited_by_count	Citation count
embedding	384-dimensional vector
created_at	Record creation timestamp
updated_at	Last update timestamp

The embedding is generated from the paper title and abstract.

5. Authors Table

The authors table stores author information.

authors
--------
id
name
orcid

Authors are shared between papers instead of being duplicated for every paper.

6. Topics Table

The topics table stores research topics associated with papers.

topics
--------
id
name

A topic can be associated with multiple papers.

7. Association Tables
paper_authors

Connects papers and authors.

paper_authors
-------------
paper_id
author_id

Relationship:

Paper 1 ──── * Author
paper_topics

Connects papers and topics.

paper_topics
------------
paper_id
topic_id

Relationship:

Paper 1 ──── * Topic
8. Vector Storage

Research-paper embeddings are stored using pgvector.

embedding VECTOR(384)

The project uses:

all-MiniLM-L6-v2

The embedding pipeline is:

Title + Abstract
       │
       ▼
Sentence Transformer
       │
       ▼
384-dimensional vector
       │
       ▼
PostgreSQL / pgvector

This enables semantic similarity search without introducing a separate vector database.

9. Similarity Search

For a user query:

User Query
    │
    ▼
Generate Query Embedding
    │
    ▼
pgvector
    │
    ▼
Compare with Paper Embeddings
    │
    ▼
Rank by Similarity
    │
    ▼
Return Similar Papers

Cosine similarity/distance is used for comparing vectors.

10. Data Integrity

The schema uses:

Primary keys
Foreign keys
Association tables
Non-null constraints
Database relationships

OpenAlex identifiers are used to identify existing papers during ingestion.

This allows the ingestion process to be re-run without intentionally creating duplicate papers.

11. Migrations

Database schema changes are managed using Alembic.

Migrations are stored under:

backend/alembic/versions/

Apply migrations:

alembic upgrade head

Docker automatically runs migrations before starting the FastAPI application:

alembic upgrade head
        ↓
uvicorn app.main:app

Tables should not be manually created for application schema changes.

12. PostgreSQL Docker Setup

Docker Compose uses:

pgvector/pgvector:pg16

Database configuration:

Database: research_radar
User: postgres
Password: postgres
Port: 5432

The PostgreSQL data directory is persisted using a Docker volume:

postgres_data

Therefore, restarting the containers does not normally remove the database contents.

13. Database Health Check

Docker checks PostgreSQL using:

pg_isready -U postgres -d research_radar

The backend waits for PostgreSQL to become healthy before running migrations.

14. Inspecting the Database

List tables:

docker compose exec postgres \
psql -U postgres -d research_radar -c "\dt"

Inspect a table:

docker compose exec postgres \
psql -U postgres -d research_radar -c "\d papers"

Check paper count:

docker compose exec postgres \
psql -U postgres -d research_radar \
-c "SELECT COUNT(*) FROM papers;"

Check authors:

docker compose exec postgres \
psql -U postgres -d research_radar \
-c "SELECT COUNT(*) FROM authors;"

Check topics:

docker compose exec postgres \
psql -U postgres -d research_radar \
-c "SELECT COUNT(*) FROM topics;"
15. Current Dataset

The ingestion pipeline currently targets approximately:

300 papers

from:

Artificial Intelligence
Natural Language Processing

The actual number can vary because OpenAlex results may change.

The ingestion process creates the corresponding authors, topics, relationships, and embeddings.

16. Design Trade-offs
PostgreSQL + pgvector

Chosen because it provides both:

Relational database functionality
Vector similarity search

This keeps the architecture simple for the size of the assignment.

Separate Author and Topic Tables

Authors and topics are normalized instead of storing duplicated text in every paper record.

This improves:

Data consistency
Filtering
Reuse
Relationship queries
Local Embeddings

Using a local Sentence Transformer avoids an external AI dependency and API cost.

For a much larger corpus, embedding generation and vector search could be moved to dedicated infrastructure.