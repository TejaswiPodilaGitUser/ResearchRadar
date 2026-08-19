# Research Radar — Frontend Documentation

Research Radar frontend is a React + TypeScript application that provides a user-friendly interface for discovering, searching, filtering, and exploring research papers.

The frontend communicates with the FastAPI backend through REST APIs and provides loading, empty, and error states for a complete user experience.

## 1. Technology Stack
Technology	Purpose
React 18	UI framework
TypeScript	Type safety
Vite	Development server and build tool
React Router	Client-side routing
Axios	HTTP communication
CSS	Application styling
Docker	Production containerization
Nginx	Production web server
## 2. Frontend Architecture
```
                         ┌──────────────────────┐
                         │      React App       │
                         │     TypeScript       │
                         └──────────┬───────────┘
                                    │
                         ┌──────────▼───────────┐
                         │    React Router      │
                         └──────────┬───────────┘
                                    │
              ┌─────────────────────┼─────────────────────┐
              │                     │                     │
              ▼                     ▼                     ▼
       ┌─────────────┐       ┌───────────────┐    ┌─────────────┐
       │ Search Page │       │ Paper Details  │    │   Metrics   │
       └──────┬──────┘       └───────┬───────┘    └──────┬──────┘
              │                      │                    │
              └──────────────────────┼────────────────────┘
                                     │
                              ┌──────▼──────┐
                              │  API Layer  │
                              │   Axios     │
                              └──────┬──────┘
                                     │
                                     │ HTTP
                                     ▼
                              ┌─────────────┐
                              │  FastAPI    │
                              │   Backend   │
                              └─────────────┘
```
## 3. Project Structure

The frontend is organized into pages, API clients, reusable components, and styles.
```
frontend/
│
├── public/
│
├── src/
│   │
│   ├── api/
│   │   ├── axiosClient.ts
│   │   ├── paperApi.ts
│   │   ├── recommendationApi.ts
│   │   ├── authorApi.ts
│   │   ├── topicApi.ts
│   │   ├── metricsApi.ts
│   │   └── apiMetrics.ts
│   │
│   ├── components/
│   │   ├── common/
│   │   │   ├── LoadingState.tsx
│   │   │   └── ErrorState.tsx
│   │   │
│   │   ├── PaperCard.tsx
│   │   ├── Pagination.tsx
│   │   ├── MetricsCards.tsx
│   │   └── ApiMetrics.tsx
│   │
│   ├── pages/
│   │   ├── SearchPage.tsx
│   │   ├── PaperDetailPage.tsx
│   │   ├── AuthorPage.tsx
│   │   ├── TopicPage.tsx
│   │   └── MetricsPage.tsx
│   │
│   ├── styles/
│   │   ├── global.css
│   │   ├── search-page.css
│   │   ├── paper-page.css
│   │   ├── author-page.css
│   │   ├── metrics.css
│   │   └── api-metrics.css
│   │
│   ├── app/
│   │   └── router.tsx
│   │
│   ├── App.tsx
│   └── main.tsx
│
├── Dockerfile
├── nginx.conf
├── package.json
├── package-lock.json
├── tsconfig.json
├── vite.config.ts
└── index.html
```
## 4. Application Routes

The application uses React Router for client-side navigation.

Main routes:
```
/
├── /search
├── /papers/:paperId
├── /authors/:authorId
├── /topics/:topicId
└── /metrics
```
## 5. Search Page

The Search page is the primary research discovery interface.

It allows users to:

Search papers
Filter results
Navigate through pages
Open paper details
Handle empty results
Handle API failures
See loading states
Search Flow
```
User enters search text
          │
          ▼
     Debounce input
          │
          ▼
     Build API query
          │
          ▼
       Axios call
          │
          ▼
       FastAPI
          │
          ▼
     Search results
          │
          ▼
      Paper cards
```
## 6. Debounced Search

The search input is debounced to avoid making an API request for every keystroke.

Example behavior:

User types:


machine
```

m
ma
mac
mach
machi
machin
machine
       │
       ▼
   debounce
       │
       ▼
one API request
```
The debounce delay is approximately:
```
400 ms
```
This reduces unnecessary backend requests and makes the search experience more responsive.

## 7. Search Filters

The Search page supports filters including:

Keyword

Searches paper content.
```
Artificial Intelligence
Machine Learning
Natural Language Processing
```
Publication Year

Example:
```
2023
2024
2025
```
Author

- Allows filtering by author.

Topic

- Allows filtering by research topic.

## 8. Pagination

Search results are displayed using pagination.

The frontend sends pagination information to the backend.

Example:
```
page=1
size=20
```
Navigation:
```
Previous | 1 | 2 | 3 | 4 | Next
```
The frontend prevents invalid page navigation.

## 9. Paper Cards

Each search result is displayed as a paper card.

Typical information includes:

Paper Title


Authors


Publication Year


Topics


Abstract Preview


Citation Count

The card provides navigation to:
```
/papers/{paperId}
```
## 10. Paper Detail Page

The Paper Detail page displays the complete information for a selected paper.

Typical information includes:
```
Title
Abstract
Authors
Topics
Publication year
Publication date
DOI
Citation count
Related research
```
## 11. Paper Detail Flow
```
User selects paper
        │
        ▼
/papers/{id}
        │
        ▼
Frontend requests:
GET /papers/{id}
        │
        ▼
FastAPI
        │
        ▼
Paper detail response
        │
        ▼
React state
        │
        ▼
Paper detail UI
```
## 12. AI / Research Discovery Feature

The frontend supports the AI-powered research discovery functionality provided by the backend.

For similarity-based discovery, the flow is:
```
Current Paper
      │
      ▼
Backend similarity API
      │
      ▼
Embedding / vector search
      │
      ▼
Similar Papers
      │
      ▼
Frontend recommendation cards
```
The goal is to allow a researcher to continue exploring related papers without manually constructing another search query.

## 13. API Layer

The frontend keeps API communication separate from page components.

Example:
```
src/api/


paperApi.ts
recommendationApi.ts
authorApi.ts
topicApi.ts
metricsApi.ts
apiMetrics.ts
```
This separation provides:

Reusable API functions
Centralized HTTP configuration
Cleaner React components
Easier error handling
Easier testing
## 14. Axios Configuration

The Axios client is responsible for communicating with the backend.

The backend URL is configured through:
```
VITE_API_BASE_URL
```
For local development:
```
VITE_API_BASE_URL=http://localhost:8000
```
For Docker development:
```
VITE_API_BASE_URL=http://localhost:8000
```
The Vite environment variable is embedded into the frontend during the build process.

## 15. Docker Environment Variable

The frontend Dockerfile accepts:
```
ARG VITE_API_BASE_URL
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL
```
Docker Compose provides the value:
```
frontend:
  build:
    context: ./frontend
    dockerfile: Dockerfile
    args:
      VITE_API_BASE_URL: http://localhost:8000
```
This is important because Vite environment variables are build-time configuration, not runtime browser environment variables.

## 16. Frontend Docker Build

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
      Nginx image
           │
           ▼
   Static React application
```
The production image does not need Node.js to serve the application.

## 17. Production Dockerfile

The frontend Dockerfile follows this structure:
```
FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./

RUN npm ci

COPY . .

ARG VITE_API_BASE_URL

ENV VITE_API_BASE_URL=$VITE_API_BASE_URL

RUN npm run build

FROM nginx:alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf

COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```
## 18. Nginx

Nginx serves the generated React static files.
```
Browser
   │
   ▼
Nginx :80
   │
   ▼
React /dist
```
The Docker host exposes:
```
localhost:5173
```
which maps to:

container:80
## 19. React Router and Nginx

Because React Router uses client-side routes, Nginx needs to return index.html when a route does not correspond to a physical file.

For example:
```
/papers/123
```
must load the React application rather than return a normal Nginx 404.

The Nginx configuration should therefore contain:
```
location / {
    try_files $uri $uri/ /index.html;
}
```
## 20. Loading States

The frontend provides explicit loading states while APIs are executing.

Example:

Loading papers...

This prevents the application from appearing frozen while waiting for the backend.

Loading states are especially important for:
```
Search
Paper details
Recommendations
Metrics
Author details
Topic details
```
## 21. Empty States

The application handles cases where an API successfully returns no results.

Example:

No papers found.


Try changing your search terms or filters.

This is preferable to showing an empty screen.

## 22. Error States

API failures are displayed through reusable error components.

Example:
```
Unable to load papers.


Please try again.
```
The frontend distinguishes between:
```
Loading
Success
Empty
Error
```
rather than treating all states as the same UI state.

## 23. API Error Handling

The API layer converts backend failures into frontend-readable errors.

Typical backend responses include:
```
400
404
422
429
500
503
```
The frontend can display appropriate messages rather than exposing raw Axios or browser errors to users.

## 24. Metrics Page

The Metrics page provides visibility into the research corpus and API performance.

Research Metrics

The frontend displays:
```
Papers
Authors
Topics
Publication Range
```
Example:
```
Papers       299
Authors    1720
Topics       741
```
```
2023 ───────── 2025
```
## 25. API Performance Metrics

The frontend also displays API performance information.

Metrics include:
```
Total Requests
Average Response Time
Errors
Error Rate
P90
P95
P99
```
Example:
```
Requests       1,248
Avg Response      85 ms
P95              180 ms
Errors             12
Error Rate       0.96%
```
The values are obtained from the backend metrics endpoint.

## 26. Frontend State Management

The application uses React component state for page-level state.

Typical state includes:
```
papers
loading
error
searchQuery
selectedYear
selectedTopic
selectedAuthor
currentPage
totalPages
```
For the current application size, a dedicated global state library is not necessary.

This keeps the frontend simpler.

## 27. API Request Lifecycle

A typical API request follows:
```
React Component
       │
       ▼
API Function
       │
       ▼
Axios Client
       │
       ▼
FastAPI
       │
       ▼
JSON Response
       │
       ▼
API Function
       │
       ▼
React State
       │
       ▼
UI
```
## 28. Search Performance

The frontend uses several mechanisms to avoid unnecessary API calls.

Debouncing

- Prevents an API call for every keystroke.

Pagination

- Avoids loading the complete dataset into the browser.

Backend Filtering

- Filtering is performed by the backend/database rather than downloading all papers.

Lazy Detail Loading

- Paper details are requested only when the user opens a paper.

## 29. Responsive Design

The frontend is designed to remain usable across:
```
Desktop
Tablet
Mobile
```
The UI uses responsive CSS for:
```
Search controls
Paper cards
Metrics cards
Detail sections
Pagination
Navigation
```
## 30. Accessibility Considerations

The frontend uses standard HTML controls and readable UI patterns.

Important considerations include:

- Labels for form controls
- Keyboard-accessible buttons
- Clear focus states
- Meaningful error messages
- Sufficient text contrast
- Semantic headings
- Accessible navigation

Accessibility can be further improved with automated accessibility testing.

## 31. Frontend Development

Navigate to:
```
cd frontend
```
Install dependencies:
```
npm install
```
Create:
```
frontend/.env
```
with:
```
VITE_API_BASE_URL=http://localhost:8000
```
Start the development server:
```
npm run dev
```
The frontend is normally available at:
```
http://localhost:5173
```
## 32. Production Build

Build the frontend locally:
```
npm run build
```
The generated application is placed in:
```
frontend/dist/
```
Preview the production build:
```
npm run preview
```
## 33. Docker Frontend

From the project root:
```
docker compose build frontend
```
Start the frontend:
```
docker compose up frontend
```
Access:
```
http://localhost:5173
```
## 34. Complete Application Startup

The recommended way to run the entire application is from the project root:
```
docker compose up --build
```
The application consists of:
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
   React Frontend
```
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
## 35. Frontend Docker Configuration

The frontend service in docker-compose.yml uses:
```
frontend:
  build:
    context: ./frontend
    dockerfile: Dockerfile
    args:
      VITE_API_BASE_URL: http://localhost:8000


  container_name: research-radar-frontend
  restart: unless-stopped


  ports:
    - "5173:80"


  depends_on:
    - backend
```
The API URL is therefore available to the React application during the Vite build.

## 36. Common Docker Issue
VITE_API_BASE_URL is not configured

If the browser displays:

Uncaught Error:
VITE_API_BASE_URL is not configured.

the frontend was built without the required Vite build argument.

Rebuild the frontend:
```
docker compose build --no-cache frontend
```
Then start:
```
docker compose up
```
Or simply:
```
docker compose up --build
```
The Compose configuration must contain:
```
args:
  VITE_API_BASE_URL: http://localhost:8000
```
## 37. Why localhost:8000?

The browser executes the frontend JavaScript on the host machine.

Therefore the browser must call:
```
http://localhost:8000
```
It should not use:
```
http://backend:8000
```
backend is a Docker Compose service name and is resolvable by containers inside the Docker network, but not by the user's browser.

The communication paths are therefore:
```
Browser
   │
   ├── localhost:5173
   │       │
   │       ▼
   │     Nginx
   │
   └── localhost:8000
           │
           ▼
        FastAPI
```
while internally Docker uses:
```
backend → postgres:5432
```
## 38. Frontend Build vs Runtime Configuration

Vite environment variables are embedded during:
```
npm run build
```
Therefore:
```
VITE_API_BASE_URL
```
must be available when the Docker image is built.

Changing the Docker Compose environment after the frontend image has already been built does not change the JavaScript bundle.

Use:
```
docker compose build --no-cache frontend
```
when changing the frontend API URL.

## 39. Frontend Error Prevention

The frontend intentionally fails fast when the API configuration is missing.

This prevents a partially configured application from silently making requests to an invalid backend.

Expected configuration:
```
VITE_API_BASE_URL=http://localhost:8000
```
## 40. Frontend Testing

Frontend tests can be added around the most important user flows.

Recommended areas:
```
Search
Pagination
Filters
Paper Details
Loading States
Empty States
API Errors
Metrics
```
The highest-value tests should verify that the user can:

Search for a paper.
Filter results.
Navigate to a paper.
View paper details.
View the AI/recommendation feature.
Recover from API failures.
## 41. Frontend Engineering Decisions
```
React + TypeScript
```
React provides a lightweight component-based UI model.

TypeScript provides compile-time checking for:

- API responses
- Component props
- State
- Function parameters
- Data transformations

Axios

- Axios provides a clean abstraction around HTTP requests and makes centralized request configuration and error handling easier.

React Router

- React Router provides client-side navigation without requiring full page reloads.

No Global State Library

- The current application does not require Redux or another global state solution.

Most state is local to individual pages.

This keeps the implementation smaller and easier to understand.

If the application grows significantly, shared state could be introduced for:

- Authentication
- User preferences
- Search state
- Global notifications
- Cached API data
## 42. Trade-offs
Client-side debounce

Debouncing improves responsiveness and reduces unnecessary backend traffic.

Trade-off:

A user may see a small delay before search results update.

Server-side pagination

Only the requested page is returned by the backend.

Advantages:

- Lower network usage
- Faster rendering
- Better scalability
- Local API state

Page-level React state keeps the application simple.

Trade-off:

Data may be fetched again when navigating between pages.

A library such as React Query could later provide:

- Request caching
- Automatic refetching
- Request deduplication
- Stale data management
## 43. Future Improvements

With additional time, the frontend could be enhanced with:

- Search
- Search result highlighting
- Advanced filters
- Saved searches
- Search history
- Better relevance indicators
- AI
- Similarity score visualization
- Explanation of why papers are similar
- Abstract summarization
- Research trend visualization
- Performance
- React Query
- Virtualized large result lists
- Lazy loading
- Code splitting
- Browser caching
- UX
- Dark mode
- Keyboard shortcuts
- Better mobile navigation
- Skeleton loaders
- Toast notifications
- Accessibility
- Automated WCAG testing
- Screen-reader optimization
- Improved keyboard navigation
## 44. Production Considerations

For a production deployment, the frontend should additionally use:

- HTTPS
- Content Security Policy
- Security headers
- Cache-control headers
- Asset compression
- CDN
- Error monitoring
- Automated frontend testing
- CI/CD
- Environment-specific configuration
## 45. Frontend Status
Completed
- React application
- TypeScript
- Vite
- React Router
- Axios API integration
- Search page
- Keyword search
- Debounced search
- Year filtering
- Topic filtering
- Author filtering
- Pagination
- Paper cards
- Paper detail page
- Author information
- Topic information
- Metrics page
- Research corpus metrics
- API performance metrics
- P90/P95/P99 metrics
- Loading states
- Empty states
- Error states
- Responsive styling
- Docker build
- Nginx production serving
- Docker Compose integration
- Vite API configuration
- Final Verification
- Fresh-clone Docker startup
- End-to-end search verification
- Paper detail verification
- AI/recommendation verification
- Frontend API error verification
- Production build verification
- Final browser smoke test
## 46. End-to-End Frontend Flow

The complete user journey is:
```
                    Research Radar
                         │
                         ▼
                  Search Page
                         │
             ┌───────────┴───────────┐
             │                       │
             ▼                       ▼
       Search / Filter          Browse Pages
             │
             ▼
       Paper Results
             │
             ▼
       Select Paper
             │
             ▼
       Paper Details
             │
      ┌──────┴────────┐
      │               │
      ▼               ▼
   Metadata      AI / Similar Papers
      │               │
      └───────┬───────┘
              ▼
        Continue Research
```
The frontend is designed around the core assignment requirement: a real user should be able to discover a paper, understand its metadata, and continue exploring related research without needing technical instructions.