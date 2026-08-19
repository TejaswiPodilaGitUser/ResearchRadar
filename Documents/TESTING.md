TESTING.md
# Research Radar — Testing


## 1. Overview


Testing focuses primarily on the backend API and the most important application flows.


The goal is to verify:


- API correctness
- Request validation
- Search and filtering
- Pagination
- Paper details
- Error handling
- Health checks
- Database integration


Full test coverage is not the goal for this assignment.


---


## 2. Testing Strategy


The project follows a layered testing approach:


```text
             Tests
               │
       ┌───────┴────────┐
       │                │
       ▼                ▼
   API Tests       Integration Tests
       │                │
       ▼                ▼
   FastAPI          PostgreSQL
   Endpoints        Database
```
The API layer receives the highest testing priority because it represents the main application contract.

## 3. API Tests

Important API scenarios include:

Health Check

Verify that the application reports a healthy status.
```
GET /health
```
Expected:
```
HTTP 200
```
Paper Listing

Verify that papers can be retrieved successfully.
```
GET /papers
```
Check:

HTTP status
Response structure
Paper records
Pagination metadata
Pagination

Example:
```
GET /papers?page=1&size=20
```
Test cases:

First page
Subsequent pages
Page size limits
Empty page
Keyword Search

Example:
```
GET /papers?keyword=machine learning
```
Verify that matching papers are returned based on title/abstract search.

Also test:

Empty keyword
Very long keyword
Unknown keyword
Filters

Test filtering by:
```
Year
Topic
Author
```
Example:
```
GET /papers?year=2024
```
Verify that returned records satisfy the requested filter.

## 4. Paper Detail Tests

Test:
```
GET /papers/{id}
```
Verify that the response contains expected metadata such as:

- Title
- Abstract
- Publication year
- DOI
- Authors
- Topics

Also test an invalid/non-existing ID.

Expected:
```
HTTP 404
```
## 5. Validation Tests

The API validates incoming parameters.

Examples include:

- Invalid page number
- Invalid page size
- Invalid year
- Excessively long search input
- Invalid IDs

Expected validation failures should return an appropriate HTTP status such as:
```
400
422
```
depending on the validation path.

## 6. Error Handling Tests

Important failure scenarios include:

- Paper not found
- Invalid request
- Database error
- Unexpected application error

The API should return structured error responses instead of exposing internal stack traces.

Example:
```
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "Paper not found"
  }
}
```
## 7. Recommendation / Similarity Tests

The similarity functionality should verify:

- Valid paper ID
- Similar papers are returned
- The requested paper is not returned as its own recommendation
- Results are limited to the expected number
- Empty results are handled correctly

Example:
```
GET /recommendations/{paper_id}/similar
```
## 8. Database Integration Tests

Database tests verify important relationships:
```
Paper
  │
  ├── Authors
  │
  └── Topics
```
Test cases include:

- Paper creation
- Author association
- Topic association
- Duplicate ingestion
- Foreign-key relationships
- Retrieval of related records
## 9. Ingestion Testing

The OpenAlex ingestion process should be safe to run multiple times.

Example:
```
python -m app.ingestion.openalex_loader
```
Run it again and verify that duplicate papers are not created.

The main idempotency check is based on the OpenAlex paper identifier.

## 10. Embedding Tests

Embedding generation should verify:

- Text is successfully converted to an embedding
- Expected dimension is 384
- Empty/invalid input is handled safely
- Existing embeddings are not unnecessarily regenerated

Expected vector dimension:
```
384
```
## 11. Frontend Testing

The frontend should be manually verified for the main user journeys.
```
Search
Open application
      ↓
Enter search term
      ↓
Apply filters
      ↓
View results
      ↓
Navigate pages
Paper Details
Search Results
      ↓
Select Paper
      ↓
Paper Detail Page
      ↓
View Metadata
      ↓
View Similar Papers
```
Also verify:

Loading state
Empty state
API error state
Invalid paper ID
Pagination
Responsive layout
## 12. Docker End-to-End Testing

The complete application should start using:
```
docker compose up --build
```
Verify:
```
PostgreSQL
    ↓
Backend
    ↓
Frontend
```
Check backend:
```
http://localhost:8000
```
Swagger:
```
http://localhost:8000/docs
```
Frontend:
```
http://localhost:5173
```
## 13. Database Verification

After ingestion:
```
docker compose exec postgres \
psql -U postgres -d research_radar \
-c "SELECT COUNT(*) FROM papers;"
```
Check related data:
```
docker compose exec postgres \
psql -U postgres -d research_radar \
-c "SELECT COUNT(*) FROM authors;"
docker compose exec postgres \
psql -U postgres -d research_radar \
-c "SELECT COUNT(*) FROM topics;"
```
## 14. Running Tests

From the backend directory:
```
pytest
```
Verbose output:
```
pytest -v
```
Run a specific test file:
```
pytest tests/test_papers.py
```
Run a specific test:
```
pytest tests/test_papers.py::test_get_papers
```
## 15. Test Priorities

The highest-priority tests are:

- Health endpoint
- Paper listing
- Pagination
- Search
- Filters
- Paper detail
- Not-found handling
- Validation
- Similar-paper recommendations
- Ingestion idempotency
## 16. Future Testing Improvements

With additional development time, the test suite could be extended with:

- Higher API coverage
- Repository/service unit tests
- Dedicated PostgreSQL test containers
- Frontend component tests
- Playwright end-to-end tests
- Load testing with JMeter
- CI test execution
- Coverage reporting

The objective would be to keep fast unit/API tests in CI while running heavier integration and end-to-end tests separately.