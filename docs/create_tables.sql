-- Create database separately
-- CREATE DATABASE research_radar;

-- Connect to database
-- \c research_radar


-- Enable vector extension for AI similarity feature
CREATE EXTENSION IF NOT EXISTS vector;


----------------------------------------------------
-- PAPERS TABLE
----------------------------------------------------

CREATE TABLE papers (
    id BIGSERIAL PRIMARY KEY,

    openalex_id VARCHAR(100) UNIQUE NOT NULL,

    title TEXT NOT NULL,

    abstract TEXT,

    publication_year INTEGER,

    publication_date DATE,

    doi VARCHAR(255),

    cited_by_count INTEGER DEFAULT 0,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE INDEX idx_papers_year
ON papers(publication_year);


CREATE INDEX idx_papers_title
ON papers(title);


----------------------------------------------------
-- AUTHORS TABLE
----------------------------------------------------

CREATE TABLE authors (

    id BIGSERIAL PRIMARY KEY,

    openalex_id VARCHAR(100),

    name VARCHAR(255) NOT NULL,

    orcid VARCHAR(255),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE INDEX idx_authors_name
ON authors(name);


----------------------------------------------------
-- TOPICS TABLE
----------------------------------------------------

CREATE TABLE topics (

    id BIGSERIAL PRIMARY KEY,

    name VARCHAR(255) UNIQUE NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE INDEX idx_topics_name
ON topics(name);


----------------------------------------------------
-- PAPER AUTHORS MAPPING TABLE
----------------------------------------------------

CREATE TABLE paper_authors (

    paper_id BIGINT NOT NULL,

    author_id BIGINT NOT NULL,


    PRIMARY KEY(
        paper_id,
        author_id
    ),


    CONSTRAINT fk_paper_author_paper
    FOREIGN KEY(paper_id)
    REFERENCES papers(id)
    ON DELETE CASCADE,


    CONSTRAINT fk_paper_author_author
    FOREIGN KEY(author_id)
    REFERENCES authors(id)
    ON DELETE CASCADE
);



----------------------------------------------------
-- PAPER TOPICS MAPPING TABLE
----------------------------------------------------

CREATE TABLE paper_topics (

    paper_id BIGINT NOT NULL,

    topic_id BIGINT NOT NULL,


    PRIMARY KEY(
        paper_id,
        topic_id
    ),


    CONSTRAINT fk_paper_topic_paper
    FOREIGN KEY(paper_id)
    REFERENCES papers(id)
    ON DELETE CASCADE,


    CONSTRAINT fk_paper_topic_topic
    FOREIGN KEY(topic_id)
    REFERENCES topics(id)
    ON DELETE CASCADE
);



----------------------------------------------------
-- PAPER EMBEDDINGS TABLE
-- Used for AI Similarity Search
----------------------------------------------------

CREATE TABLE paper_embeddings (

    id BIGSERIAL PRIMARY KEY,


    paper_id BIGINT UNIQUE NOT NULL,


    embedding VECTOR(384),


    model_name VARCHAR(100)
    DEFAULT 'all-MiniLM-L6-v2',


    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,


    CONSTRAINT fk_embedding_paper
    FOREIGN KEY(paper_id)
    REFERENCES papers(id)
    ON DELETE CASCADE
);



----------------------------------------------------
-- SAMPLE DATA CHECK
----------------------------------------------------

SELECT table_name
FROM information_schema.tables
WHERE table_schema='public';