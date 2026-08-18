"""
OpenAlex ingestion pipeline.

Responsibilities:

1. Fetch research papers from OpenAlex API
2. Transform response data
3. Store papers, authors, topics
4. Generate embeddings for AI similarity search
5. Avoid duplicate records (idempotent ingestion)
"""

import os

import httpx

from datetime import datetime, timezone

from dotenv import load_dotenv

from sqlalchemy.orm import Session


from app.ai.embedding_service import embedding_service

from app.database.database import SessionLocal

from app.models.paper import Paper
from app.models.author import Author
from app.models.topic import Topic


load_dotenv()


OPENALEX_URL = os.getenv(
    "OPENALEX_BASE_URL",
    "https://api.openalex.org"
)


TOPICS = [
    "artificial intelligence",
    "natural language processing"
]


MAX_RESULTS = 300



# =====================================================
# Fetch OpenAlex Papers
# =====================================================

def fetch_openalex_papers():

    papers = []


    with httpx.Client(timeout=30) as client:


        for topic in TOPICS:


            params = {

                "search": topic,

                "filter":
                "from_publication_date:2023-01-01",

                "per-page":150
            }


            response = client.get(
                f"{OPENALEX_URL}/works",
                params=params
            )


            response.raise_for_status()


            data = response.json()


            papers.extend(
                data.get("results", [])
            )


    return papers[:MAX_RESULTS]



# =====================================================
# Extract Abstract
# =====================================================

def extract_abstract(
        paper_data: dict
):

    """
    OpenAlex stores abstract
    as inverted index.
    Convert to normal text.
    """


    inverted_index = (
        paper_data.get(
            "abstract_inverted_index"
        )
    )


    if not inverted_index:

        return None



    words = []


    for word, positions in inverted_index.items():

        for position in positions:

            words.append(
                (
                    position,
                    word
                )
            )


    words.sort(
        key=lambda x:x[0]
    )


    return " ".join(
        word
        for _, word in words
    )



# =====================================================
# Author
# =====================================================

def get_or_create_author(
        db: Session,
        author_data: dict
):
    """
    Get or create an author using the fields that exist
    in the current Author model.

    Author table:
        id
        name
        orcid
    """

    name = author_data.get("display_name")
    orcid = author_data.get("orcid")

    if not name:
        return None

    # Prefer ORCID when available because it is a stable
    # identifier for an author.
    if orcid:
        author = (
            db.query(Author)
            .filter(
                Author.orcid == orcid
            )
            .first()
        )

        if author:
            return author

    # Fallback to author name.
    author = (
        db.query(Author)
        .filter(
            Author.name == name
        )
        .first()
    )

    if author:
        return author

    # Create new author using ONLY fields
    # that exist in the Author model.
    author = Author(
        name=name,
        orcid=orcid
    )

    db.add(author)
    db.flush()

    return author
# =====================================================
# Topic
# =====================================================

def get_or_create_topic(
        db: Session,
        topic_name: str
):


    if not topic_name:

        return None



    topic = (

        db.query(Topic)

        .filter(
            Topic.name == topic_name
        )

        .first()
    )



    if topic:

        return topic



    topic = Topic(
        name=topic_name
    )


    db.add(topic)

    db.flush()


    return topic



# =====================================================
# Save Paper
# =====================================================

def save_paper(
        db: Session,
        paper_data: dict
):


    openalex_id = paper_data.get(
        "id"
    )


    if not openalex_id:

        return None



    existing = (

        db.query(Paper)

        .filter(
            Paper.openalex_id == openalex_id
        )

        .first()
    )



    abstract = extract_abstract(
        paper_data
    )


    text = (

        (paper_data.get("title") or "")

        +

        " "

        +

        (abstract or "")
    )



    embedding = (

        embedding_service
        .generate_embedding(
            text
        )
    )



    # -----------------------------------------
    # Existing Paper
    # -----------------------------------------

    if existing:


        if not existing.embedding:

            existing.embedding = embedding


        existing.updated_at = (
            datetime.now(timezone.utc)
        )


        return existing



    # -----------------------------------------
    # New Paper
    # -----------------------------------------

    paper = Paper(

        openalex_id=openalex_id,


        title=paper_data.get(
            "title"
        ),


        abstract=abstract,


        embedding=embedding,


        publication_year=
        paper_data.get(
            "publication_year"
        ),


        doi=
        paper_data.get(
            "doi"
        ),


        cited_by_count=
        paper_data.get(
            "cited_by_count",
            0
        ),


        created_at=datetime.now(
            timezone.utc
        ),


        updated_at=datetime.now(
            timezone.utc
        )
    )


    db.add(paper)

    db.flush()



    # -----------------------------------------
    # Authors
    # -----------------------------------------

    added_author_ids = set()


    for item in paper_data.get(
        "authorships",
        []
    ):


        author_info = item.get(
            "author"
        )


        if not author_info:

            continue



        author_id = author_info.get(
            "id"
        )


        if (
            not author_id
            or author_id in added_author_ids
        ):

            continue



        author = get_or_create_author(
            db,
            author_info
        )


        if author:

            paper.authors.append(
                author
            )


            added_author_ids.add(
                author_id
            )



    # -----------------------------------------
    # Topics
    # -----------------------------------------

    added_topics = set()



    for concept in paper_data.get(
        "concepts",
        []
    ):


        topic_name = concept.get(
            "display_name"
        )


        if not topic_name:

            continue



        if topic_name in added_topics:

            continue



        topic = get_or_create_topic(
            db,
            topic_name
        )


        if topic:

            paper.topics.append(
                topic
            )


            added_topics.add(
                topic_name
            )



    return paper



# =====================================================
# Main
# =====================================================

def run_ingestion():


    db = SessionLocal()


    try:


        papers = fetch_openalex_papers()


        print(
            f"Fetched {len(papers)} papers"
        )



        count = 0



        for paper_data in papers:


            save_paper(
                db,
                paper_data
            )


            count += 1



        db.commit()



        print(
            f"Processed {count} papers"
        )



    except Exception as e:


        db.rollback()


        print(
            "Ingestion failed:",
            e
        )


        raise



    finally:


        db.close()



if __name__ == "__main__":

    run_ingestion()