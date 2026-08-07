"""
OpenAlex ingestion pipeline.

Responsibilities:
1. Fetch research papers from OpenAlex API
2. Transform response data
3. Store papers, authors, topics
4. Avoid duplicate records (idempotent ingestion)
"""

import os

import httpx

from datetime import datetime, timezone
from dotenv import load_dotenv

from sqlalchemy.orm import Session

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



def fetch_openalex_papers():

    """
    Fetch papers from OpenAlex API
    """

    papers = []


    for topic in TOPICS:

        params = {
            "search": topic,
            "filter": "from_publication_date:2023-01-01",
            "per-page": 150
        }


        response = httpx.get(
            f"{OPENALEX_URL}/works",
            params=params,
            timeout=30
        )


        response.raise_for_status()


        data = response.json()


        papers.extend(
            data.get("results", [])
        )


    return papers[:MAX_RESULTS]



def get_or_create_author(
        db: Session,
        author_data: dict
):

    """
    Insert author if not exists
    """

    openalex_id = author_data.get("id")


    if not openalex_id:
        return None


    author = (
        db.query(Author)
        .filter(
            Author.openalex_id == openalex_id
        )
        .first()
    )


    if author:
        return author


    author = Author(
        openalex_id=openalex_id,
        name=author_data.get(
            "display_name"
        )
    )


    db.add(author)

    db.flush()


    return author



def get_or_create_topic(
        db: Session,
        topic_name: str
):

    """
    Insert topic if not exists
    """

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



def save_paper(
        db: Session,
        paper_data: dict
):

    """
    Save single paper
    """


    openalex_id = paper_data.get(
        "id"
    )


    existing = (
        db.query(Paper)
        .filter(
            Paper.openalex_id == openalex_id
        )
        .first()
    )


    # Idempotency check
    if existing:
        return existing



    paper = Paper(

        openalex_id=openalex_id,

        title=paper_data.get(
            "title"
        ),

        abstract=None,

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



    #
    # Save Authors
    #

    authorships = paper_data.get(
        "authorships",
        []
    )


    added_author_ids = set()


    for item in authorships:

        author_info = item.get(
            "author"
        )


        if not author_info:
            continue


        author_openalex_id = (
            author_info.get("id")
        )


        if (
            not author_openalex_id
            or author_openalex_id in added_author_ids
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
                author_openalex_id
            )



    #
    # Save Topics
    #

    concepts = paper_data.get(
        "concepts",
        []
    )


    added_topics = set()


    for concept in concepts:


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



def run_ingestion():

    """
    Main ingestion workflow
    """

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
            f"Inserted {count} papers"
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