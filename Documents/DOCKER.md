Research Radar — Docker Setup

This document explains how to build, start, stop, reset, and troubleshoot the complete Research Radar application using Docker Compose.

## 1. Docker Architecture

Research Radar runs as three Docker services:
```
                    ┌──────────────────────┐
                    │      Frontend        │
                    │   React + Nginx      │
                    │      Port 5173       │
                    └──────────┬───────────┘
                               │
                               │ HTTP
                               ▼
                    ┌──────────────────────┐
                    │       Backend        │
                    │ FastAPI + Uvicorn    │
                    │      Port 8000       │
                    └──────────┬───────────┘
                               │
                               │ PostgreSQL
                               ▼
                    ┌──────────────────────┐
                    │      PostgreSQL      │
                    │       pgvector       │
                    │      Port 5432       │
                    └──────────────────────┘
```
Services:
```
Service	Technology	Port
postgres	PostgreSQL + pgvector	5432
backend	FastAPI + Uvicorn	8000
frontend	React + Nginx	5173
```
## 2. Prerequisites

Install:
```
Docker Desktop
Docker Compose
```
Verify Docker:
```
docker --version
```
Verify Docker Compose:
```
docker compose version
```
## 3. Project Structure

The Docker configuration is located at the project root:
```
ResearchRadar/
│
├── backend/
│   ├── Dockerfile
│   ├── alembic/
│   ├── app/
│   ├── requirements.txt
│   └── ...
│
├── frontend/
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── package.json
│   └── ...
│
├── docker-compose.yml
├── README.md
└── Documentation/
    ├── BACKEND.md
    ├── FRONTEND.md
    └── Docker.md
```
## 4. Docker Compose Configuration

The root docker-compose.yml defines:
```
postgres
backend
frontend
```
The backend connects to PostgreSQL using the Docker service name:

postgres

Therefore, inside Docker the database URL is:
```
postgresql://postgres:postgres@postgres:5432/research_radar
```
Do not use localhost for the PostgreSQL hostname from inside the backend container.

## 5. Start the Application

From the project root:
```
docker compose up --build
```
This builds the backend and frontend images and starts all services.

For detached mode:
```
docker compose up --build -d
```
## 6. Start Without Rebuilding

If Docker images have already been built:
```
docker compose up
```
Detached:
```
docker compose up -d
```
## 7. Application URLs

After startup:
```
Frontend
http://localhost:5173
Backend
http://localhost:8000
Swagger
http://localhost:8000/docs
OpenAPI
http://localhost:8000/openapi.json
PostgreSQL
localhost:5432
```
## 8. Check Running Containers
```
docker compose ps
```
Expected services:
```
research-radar-postgres
research-radar-backend
research-radar-frontend
```
For more detailed information:
```
docker ps
```
## 9. View Logs
All services
docker compose logs

Follow logs:
```
docker compose logs -f
Backend
docker compose logs backend
```
Follow backend logs:
```
docker compose logs -f backend
Frontend
docker compose logs frontend
PostgreSQL
docker compose logs postgres
```
## 10. Check PostgreSQL Health

The PostgreSQL container has a health check using:

pg_isready

Check service status:

docker compose ps

The PostgreSQL service should eventually show:

healthy
## 11. Database Access

Connect directly to PostgreSQL:
```
docker compose exec postgres \
psql -U postgres -d research_radar
```
Run a command directly:
```
docker compose exec postgres \
psql -U postgres -d research_radar -c "\dt"
```
Check tables:
```
docker compose exec postgres \
psql -U postgres -d research_radar -c "\dt"
```
Check the authors table:
```
docker compose exec postgres \
psql -U postgres -d research_radar -c "\d authors"
```
Check papers:
```
docker compose exec postgres \
psql -U postgres -d research_radar -c "\d papers"
```
## 12. Check Data

Count papers:
```
docker compose exec postgres \
psql -U postgres -d research_radar \
-c "SELECT COUNT(*) FROM papers;"
```
Count authors:
```
docker compose exec postgres \
psql -U postgres -d research_radar \
-c "SELECT COUNT(*) FROM authors;"
```
Count topics:
```
docker compose exec postgres \
psql -U postgres -d research_radar \
-c "SELECT COUNT(*) FROM topics;"
```
Check paper records:
```
docker compose exec postgres \
psql -U postgres -d research_radar \
-c "SELECT id, title, publication_year FROM papers LIMIT 10;"
```
## 13. Alembic Migrations

The backend container runs:
```
alembic upgrade head
```
before starting FastAPI.

The Docker startup sequence is:
```
Backend container starts
        │
        ▼
Wait for PostgreSQL health
        │
        ▼
alembic upgrade head
        │
        ▼
Start Uvicorn
        │
        ▼
FastAPI available on port 8000
```
This ensures the database schema is migrated before the API starts.

## 14. Check Alembic Version

Run:
```
docker compose exec backend alembic current
```
Check migration history:
```
docker compose exec backend alembic history
```
Upgrade migrations manually:

docker compose exec backend alembic upgrade head
## 15. Run Data Ingestion

After the database schema is available, run the OpenAlex ingestion process:
```
docker compose exec backend \
python -m app.ingestion.openalex_loader
```
The ingestion process:
```
OpenAlex
   │
   ▼
Fetch papers
   │
   ▼
Create/update papers
   │
   ├── Authors
   │
   └── Topics
   │
   ▼
Generate embeddings
   │
   ▼
PostgreSQL + pgvector
```
## 16. Verify Ingestion

After ingestion:
```
docker compose exec postgres \
psql -U postgres -d research_radar \
-c "SELECT COUNT(*) FROM papers;"
```
Authors:
```
docker compose exec postgres \
psql -U postgres -d research_radar \
-c "SELECT COUNT(*) FROM authors;"
```
Topics:
```
docker compose exec postgres \
psql -U postgres -d research_radar \
-c "SELECT COUNT(*) FROM topics;"
```
## 17. Frontend Environment Variable

The React/Vite application requires:
```
VITE_API_BASE_URL
```
The Docker Compose configuration passes:
```
args:
  VITE_API_BASE_URL: http://localhost:8000
```
This value is provided during the frontend Docker build.

The important distinction is:
```
Browser → localhost:8000
```
versus:
```
Docker container → backend:8000
```
Because the React application runs in the user's browser, the browser must access the backend through:
```
http://localhost:8000
```
It should not use:
```
http://backend:8000
```
for the browser API URL.

## 18. Frontend Docker Build

The frontend uses a multi-stage Docker build.
```
Node.js
   │
   ├── Install dependencies
   ├── Copy source
   └── npm run build
             │
             ▼
          /dist
             │
             ▼
        Nginx Alpine
             │
             ▼
        Port 80
```
The final container does not need Node.js to serve the application.

This keeps the runtime image smaller.

## 19. Backend Docker Build

The backend Dockerfile installs the Python dependencies and copies the application into:
```
/app
```
The backend is exposed on:
```
8000
```
Uvicorn starts with:
```
uvicorn app.main:app --host 0.0.0.0 --port 8000
```
0.0.0.0 is required so that the API is reachable outside the container.

## 20. PostgreSQL + pgvector

The PostgreSQL service uses:
```
pgvector/pgvector:pg16
```
This provides PostgreSQL 16 with the pgvector extension.

The vector column used by the application is:
```
VECTOR(384)
```
The embedding model currently generates:
```
384-dimensional embeddings
```
## 21. PostgreSQL Extension Check

Check that pgvector is available:
```
docker compose exec postgres \
psql -U postgres -d research_radar \
-c "SELECT extname FROM pg_extension;"
```
You should see:

vector

If necessary:
```
docker compose exec postgres \
psql -U postgres -d research_radar \
-c "CREATE EXTENSION IF NOT EXISTS vector;"
```
## 22. Stop the Application

Stop containers:
```
docker compose down
```
This removes the containers and network but normally keeps the PostgreSQL named volume.

## 23. Stop and Remove Database Data

Warning: This deletes the PostgreSQL data stored in the Docker volume.
```
docker compose down -v
```
Then start fresh:
```
docker compose up --build
```
This creates a completely new PostgreSQL database.

## 24. Complete Clean Restart

When Docker state becomes inconsistent, use:
```
docker compose down -v
```
Then:
```
docker compose build --no-cache
```
Then:
```
docker compose up
```
This is useful when debugging:

Old database schema
Old migration state
Old frontend build
Cached Docker layers
Dependency changes
## 25. Remove Containers

List containers:
```
docker compose ps -a
```
Remove project containers:
```
docker compose down
```
Remove stopped containers:
```
docker container prune
```
Docker will ask for confirmation.

## 26. Remove Project Images

List images:

docker images

Remove unused Docker images:
```
docker image prune
```
Remove all unused images:
```
docker image prune -a
```
Use the -a option carefully because it can remove images used by other projects if they are not currently referenced.

## 27. Remove Unused Docker Resources

To remove unused containers, networks, images, and build cache:
```
docker system prune
```
More aggressive cleanup:
```
docker system prune -a
```
To also remove unused volumes:
```
docker system prune -a --volumes
```
Warning: The last command can delete database volumes from other Docker projects.

## 28. Debug Backend Container

Open a shell:
```
docker compose exec backend sh
```
Check application files:
```
ls -la /app
```
Check Alembic:
```
ls -la /app/alembic
```
Check migrations:
```
ls -la /app/alembic/versions
```
Check Python:
```
python --version
```
Check installed packages:
```
pip list
```
## 29. Debug Frontend Container

Open a shell:
```
docker compose exec frontend sh
```
Check Nginx:
```
nginx -t
```
Check generated frontend:
```
ls -la /usr/share/nginx/html
```
Check Nginx configuration:
```
cat /etc/nginx/conf.d/default.conf
```
## 30. Test Backend From Host

Health endpoint:
```
curl http://localhost:8000/health
```
Swagger:
```
http://localhost:8000/docs
```
Paper API:
```
curl http://localhost:8000/papers
```
## 31. Test Backend From Docker

From the backend container:
```
docker compose exec backend \
python -c "import urllib.request; print(urllib.request.urlopen('http://localhost:8000/health').read().decode())"
```
Check PostgreSQL connectivity from backend:
```
docker compose exec backend \
python -c "import os; print(os.getenv('DATABASE_URL'))"
```
Expected:
```
postgresql://postgres:postgres@postgres:5432/research_radar
```
## 32. Common Problem: VITE_API_BASE_URL is not configured

Error:

Uncaught Error: VITE_API_BASE_URL is not configured.

This means the Vite variable was not available during the frontend build.

The frontend Dockerfile must contain:
```
ARG VITE_API_BASE_URL
```
```
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL
```
And docker-compose.yml must contain:
```
frontend:
  build:
    context: ./frontend
    dockerfile: Dockerfile
    args:
      VITE_API_BASE_URL: http://localhost:8000
```
After changing either file, rebuild:
```
docker compose build --no-cache frontend
```
Then:
```
docker compose up
```
## 33. Common Problem: Browser Cannot Reach Backend

Do not configure the browser with:
```
http://backend:8000
```
The Docker service name backend is only resolvable inside the Docker network.

The browser should use:
```
http://localhost:8000
```
Therefore:
```
VITE_API_BASE_URL: http://localhost:8000
```
is correct for local Docker development.

## 34. Common Problem: type "vector" does not exist

Error:
```
psycopg2.errors.UndefinedObject:
type "vector" does not exist
```
Check the PostgreSQL image:
```
docker compose exec postgres \
psql -U postgres -d research_radar \
-c "SELECT version();"
```
Check pgvector:
```
docker compose exec postgres \
psql -U postgres -d research_radar \
-c "SELECT * FROM pg_available_extensions WHERE name = 'vector';"
```
Check installed extension:
```
docker compose exec postgres \
psql -U postgres -d research_radar \
-c "SELECT * FROM pg_extension WHERE extname = 'vector';"
```
If it is not installed:
```
docker compose exec postgres \
psql -U postgres -d research_radar \
-c "CREATE EXTENSION IF NOT EXISTS vector;"
```
## 35. Common Problem: Migration Tries to Drop Non-existent Table

Example:

table "paper_embeddings" does not exist

This normally means the migration history does not match the actual database schema.

Check migration version:
```
docker compose exec postgres \
psql -U postgres -d research_radar \
-c "SELECT * FROM alembic_version;"
```
Check tables:
```
docker compose exec postgres \
psql -U postgres -d research_radar \
-c "\dt"
```
For a fresh assignment database, the simplest clean reset is:
```
docker compose down -v
```
Then:
```
docker compose up --build
```
This recreates the database and runs the current migration chain from the beginning.

## 36. Common Problem: Empty Database

Docker starting successfully does not automatically mean research data has been ingested.

The sequence is:
```
docker compose up
       │
       ▼
PostgreSQL
       │
       ▼
Alembic migrations
       │
       ▼
FastAPI
       │
       ▼
Database schema exists
       │
       ▼
Run OpenAlex ingestion
       │
       ▼
Research data
```
Run:
```
docker compose exec backend \
python -m app.ingestion.openalex_loader
```
Then verify:
```
docker compose exec postgres \
psql -U postgres -d research_radar \
-c "SELECT COUNT(*) FROM papers;"
```
37. Recommended Fresh Start

For a completely clean local environment:
```
docker compose down -v
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
Check logs:
```
docker compose logs -f backend
```
Run ingestion:
```
docker compose exec backend \
python -m app.ingestion.openalex_loader
```
Verify data:
```
docker compose exec postgres \
psql -U postgres -d research_radar \
-c "SELECT COUNT(*) FROM papers;"
```
Open:
```
http://localhost:5173
```
## 38. Recommended Normal Startup

For normal development, use:
```
docker compose up -d
```
Check:
```
docker compose ps
```
Then open:
```
http://localhost:5173
```
No database reset is required.

## 39. Recommended Submission Verification

Before submitting the project, test from a clean Docker state:
```
docker compose down -v
```
Then:
```
docker compose build --no-cache
```
Then:
```
docker compose up -d
```
Check:
```
docker compose ps
```
Verify database:
```
docker compose exec postgres \
psql -U postgres -d research_radar -c "\dt"
```
Run ingestion:
```
docker compose exec backend \
python -m app.ingestion.openalex_loader
```
Verify papers:
```
docker compose exec postgres \
psql -U postgres -d research_radar \
-c "SELECT COUNT(*) FROM papers;"
```
Verify API:
```
curl http://localhost:8000/health
```
Finally open:
```
http://localhost:5173
```
Test:
```
Search
  ↓
Filters
  ↓
Pagination
  ↓
Paper details
  ↓
AI / similarity feature
```
## 40. One-Command Startup Goal

The assignment requires the stack to come up with:
```
docker compose up
```
The intended architecture is therefore:
```
docker compose up
       │
       ├── PostgreSQL + pgvector
       │
       ├── Alembic migrations
       │
       ├── FastAPI
       │
       └── React + Nginx
```
The OpenAlex ingestion is intentionally a separate command because external data ingestion should not happen automatically every time the application containers restart.

After the first startup:
```
docker compose exec backend \
python -m app.ingestion.openalex_loader
```
This keeps application startup deterministic while still making data population simple.