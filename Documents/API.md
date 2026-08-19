API.md
# Research Radar — API Documentation


## 1. Overview


Research Radar provides REST APIs using **FastAPI**.

Base URL:

text
```
http://localhost:8000
```
Interactive API documentation:
```
http://localhost:8000/docs
```

OpenAPI specification:
```
http://localhost:8000/openapi.json
```
## 2. API Structure
```
/api
 ├── /papers
 ├── /authors
 ├── /topics
 ├── /recommendations
 ├── /search
 └── /metrics
```
## 3. Health API
```
GET /health
```
Checks whether the backend application is running.
```
Response
{
  "status": "UP"
}
```
## 4. Papers API
```
GET /papers
```
Returns a paginated list of research papers.

Query Parameters
Parameter	Description
page	Page number
size	Number of results per page
keyword	Search title and abstract
year	Filter by publication year
topic	Filter by topic
author	Filter by author
Example
```
GET /api/papers?page=1&size=20
```
Search:
```
GET /api/papers?keyword=machine%20learning
```
Filter by year:
```
GET /api/papers?year=2024
```
Filter by topic:
```
GET /api/papers?topic=natural%20language%20processing
```
Filter by author:
```
GET /api/papers?author=John
```
## 5. Paper Details
```
GET /papers/{paper_id}
```
Returns complete information about a paper.

Example
```
GET /api/papers/1
```
```
Response
{
  "id": 1,
  "title": "Example Research Paper",
  "abstract": "Research paper abstract...",
  "publication_year": 2024,
  "publication_date": "2024-05-10",
  "doi": "https://doi.org/example",
  "cited_by_count": 10,
  "authors": [],
  "topics": []
}
```
If the paper does not exist:
```
404 Not Found
```
## 6. Search API

Research Radar supports keyword and semantic search.
```
GET /search
```
Searches the research corpus.

Example:
```
GET /api/search?q=large%20language%20models
```
The semantic search flow is:
```
Query
  ↓
Embedding Model
  ↓
Query Vector
  ↓
pgvector
  ↓
Similarity Search
  ↓
Relevant Papers
```
## 7. Hybrid Search
```
GET /search/hybrid
```
Combines keyword relevance with semantic similarity.

Example:
```
GET /api/search/hybrid?q=large%20language%20models
```
Conceptually:
```
Keyword Search
      +
Semantic Search
      ↓
Combined Ranking
```
This helps when exact keyword matching alone does not provide the best research results.

## 8. Recommendations API
```
GET /recommendations/{paper_id}/similar
```
Returns papers similar to the selected paper.

Example:
```
GET /api/recommendations/1/similar
```
The recommendation process uses paper embeddings and vector similarity.

Typical flow:
```
Selected Paper
      ↓
Paper Embedding
      ↓
pgvector Similarity
      ↓
Top Similar Papers
```

```
GET /recommendations/trending
```
Returns research papers/topics considered relevant based on available corpus metadata.
```
GET /recommendations/emerging-topics
```
Returns emerging topics based on the available research dataset.
```
GET /recommendations/{topic_id}/similar
```
Returns papers associated with or related to a topic.

Example:
```
GET /api/recommendations/10/similar
```
## 9. Authors API
```
GET /authors
```
Returns authors available in the research corpus.

Example:
```
GET /api/authors
GET /authors/{author_id}
```
Returns information about a specific author.

Example:
```
GET /api/authors/10
```
## 10. Topics API
```
GET /topics
```
Returns topics available in the corpus.

Example:
```
GET /api/topics
GET /topics/{topic_id}
```
Returns details for a specific topic.

Example:
```
GET /api/topics/10
```
## 11. Metrics API
```
GET /metrics
```
Returns research corpus statistics.
```
Example:

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
## 12. API Performance Metrics
```
GET /metrics/performance
```
Returns application-level API performance metrics.

Example:
```
{
  "requests": 1248,
  "avg_response_ms": 85,
  "p95_latency_ms": 180,
  "p99_latency_ms": 250,
  "errors": 12,
  "error_rate": 0.96
}
```
Tracked metrics include:

- Total requests
- Average response time
- P90 latency
- P95 latency
- P99 latency
- Error count
- Error rate

The current implementation stores metrics in memory.

## 13. Request Tracking

API requests can include:
```
X-Request-ID: 12345
```
The backend middleware tracks the request and returns the request ID in the response.

This helps with troubleshooting and request correlation.

## 14. Pagination

Paginated endpoints use page and size parameters.

Example:
```
GET /api/papers?page=2&size=20
```
Conceptually:
```
Page 1 → Records 1–20
Page 2 → Records 21–40
Page 3 → Records 41–60
```
Pagination limits are applied to prevent excessively large responses.

## 15. Error Handling

The API uses structured error responses.

Example:
```
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "Paper not found"
  }
}
```
Common HTTP status codes:
```
Status	Meaning
200	Successful request
400	Invalid request
404	Resource not found
422	Validation error
429	Rate limit exceeded
500	Internal server error
503	Service unavailable
```
## 16. Validation

API parameters are validated before reaching the business logic.

Examples:

Invalid page
Invalid page size
Invalid year
Invalid resource ID
Excessively long search query
Invalid filter values

This prevents invalid requests from unnecessarily reaching the database.

## 17. API Flow

A typical paper-search request follows:
```
React Frontend
      │
      │ GET /api/papers
      ▼
FastAPI Router
      │
      ▼
Validation
      │
      ▼
Service Layer
      │
      ▼
SQLAlchemy
      │
      ▼
PostgreSQL
      │
      ▼
Response Schema
      │
      ▼
JSON Response
      │
      ▼
React UI
```

## 18. API Documentation

FastAPI automatically generates interactive documentation.

Open:
```
http://localhost:8000/docs
```
The documentation allows developers to:

View endpoints
Inspect request parameters
Execute API calls
View response schemas
Test APIs interactively