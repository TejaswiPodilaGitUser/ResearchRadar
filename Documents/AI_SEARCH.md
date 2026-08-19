AI_SEARCH.md
# Research Radar — AI / Semantic Search


## 1. Overview


Research Radar uses semantic search to find research papers based on meaning rather than only exact keyword matches.


The implementation uses:


- Sentence Transformers
- `all-MiniLM-L6-v2`
- PostgreSQL
- pgvector
- Cosine similarity


The embedding dimension is:

```
text
```
384
## 2. Why Semantic Search?

Traditional keyword search depends on exact words.

For example:

Query:
"AI models understanding human language"

A paper may discuss:

"Natural Language Processing using Transformer architectures"

Even though the wording is different, the concepts are related.

Semantic search helps identify this relationship.

## 3. Embedding Pipeline

Each paper is converted into a vector during ingestion.

```
Paper
  │
  ├── Title
  │
  └── Abstract
       │
       ▼
Sentence Transformer
       │
       ▼
384-dimensional Embedding
       │
       ▼
PostgreSQL + pgvector

```
The text used for embedding is:

Title + Abstract
## 4. Embedding Model

The project uses:

```
all-MiniLM-L6-v2
```
The model is provided by Sentence Transformers.

Advantages:

Runs locally
No external API key
Low resource requirements
Fast enough for the assignment
Produces fixed-size embeddings

Output:
```
384 dimensions
```
## 5. Storing Embeddings

Embeddings are stored in the papers table:

embedding VECTOR(384)

PostgreSQL with pgvector allows vector operations directly in the database.

This avoids adding a separate vector database for the current corpus size.

## 6. Query Search Flow

When a user performs a semantic search:
```
User Query
     │
     ▼
Embedding Service
     │
     ▼
Query Embedding
     │
     ▼
pgvector
     │
     ▼
Compare Against Paper Embeddings
     │
     ▼
Rank Results
     │
     ▼
Return Papers
```
## 7. Similar Paper Search

The same approach is used to find papers similar to a selected paper.
```
Selected Paper
      │
      ▼
Existing Paper Embedding
      │
      ▼
pgvector Similarity Search
      │
      ▼
Nearest Paper Embeddings
      │
      ▼
Top Similar Papers
```
The selected paper itself is excluded from the recommendation results.

## 8. Cosine Similarity

The application uses vector similarity to determine how closely two papers are related.

Conceptually:

Similarity(Query Vector, Paper Vector)

Higher similarity means the vectors are closer in semantic space.

The database performs the vector comparison, allowing the application to avoid loading the entire corpus into application memory.

9. Keyword vs Semantic Search
Keyword Search
```
Query
  ↓
Title / Abstract
  ↓
Text Matching
```
Advantages:

Exact terminology
Simple
Fast
Predictable

Limitation:

May miss conceptually related papers with different wording.
Semantic Search
```
Query
  ↓
Embedding
  ↓
Vector Similarity
```
Advantages:

Understands semantic relationships
Handles different wording
Useful for research discovery

Limitation:

Requires embedding generation
Results can be less predictable than exact matching
## 10. Hybrid Search

Research Radar can combine keyword and semantic search.
```
                 User Query
                     │
            ┌────────┴────────┐
            ▼                 ▼
      Keyword Search    Semantic Search
            │                 │
            └────────┬────────┘
                     ▼
               Combined Rank
                     │
                     ▼
                  Results
```
This provides a balance between exact matching and semantic relevance.

## 11. Ingestion and Embeddings

During OpenAlex ingestion:
```
OpenAlex Paper
      │
      ▼
Extract Title
      +
Extract Abstract
      │
      ▼
Generate Embedding
      │
      ▼
Save Paper + Embedding
```
For an existing paper, the ingestion process avoids unnecessarily recreating the paper record.

## 12. Missing Embeddings

If a paper exists without an embedding, the embedding generation process can create the missing vector.

This is useful when:

A paper was imported before embeddings were enabled
Embedding generation failed
A new embedding model is introduced
## 13. AI Feature

The selected AI-powered feature for Research Radar is:

Find Similar Papers

Given a paper, the system finds relevant papers from the existing research corpus using semantic embeddings.

Example:
```
Paper:"Transformer Models for Natural Language Processing"
        ↓
Embedding
        ↓
pgvector similarity search
        ↓
Top similar papers
```
The results are displayed on the paper detail page.

## 14. Limitations

The current implementation is intentionally simple.

Potential limitations include:

- all-MiniLM-L6-v2 is a relatively small embedding model
- Similarity depends on the quality of the paper abstract/title
- The corpus is relatively small
- No domain-specific fine-tuning is performed
- Semantic similarity does not necessarily mean scientific equivalence

Therefore, recommendations should be treated as discovery suggestions rather than authoritative research relationships.

## 15. Why pgvector Instead of a Vector Database?

For the current assignment, PostgreSQL + pgvector is sufficient.

It provides:

- Relational storage
- Vector storage
- Similarity queries
- One operational dependency
- Simple local development

For millions or billions of vectors, a dedicated vector-search architecture could be evaluated.

## 16. Future Improvements

Possible improvements include:

- Better domain-specific embedding models
- Hybrid ranking optimization
- Reciprocal Rank Fusion
- Cross-encoder re-ranking
- Query expansion
- Citation-aware recommendations
- Topic-aware similarity
- Research trend analysis
- Dedicated vector infrastructure at larger scale

The current implementation intentionally keeps the AI architecture simple, explainable, and appropriate for the assignment scope.


