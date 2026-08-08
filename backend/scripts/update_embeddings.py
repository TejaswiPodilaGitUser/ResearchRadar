from sqlalchemy import select

from app.database.database import SessionLocal
from app.models.paper import Paper
from app.ai.embedding_service import embedding_service


BATCH_SIZE = 50


def build_embedding_text(paper: Paper) -> str:
    """
    Build the text used for semantic search.
    """

    title = paper.title or ""
    abstract = paper.abstract or ""

    return f"{title}\n\n{abstract}".strip()


def update_embeddings():
    """
    Generate embeddings for papers that don't have one.
    """

    db = SessionLocal()

    try:
        papers = (
            db.query(Paper)
            .filter(Paper.embedding.is_(None))
            .all()
        )

        total = len(papers)

        print(f"Papers requiring embeddings: {total}")

        if total == 0:
            print("All papers already have embeddings.")
            return

        updated = 0

        for paper in papers:

            text = build_embedding_text(paper)

            if not text:
                continue

            paper.embedding = (
                embedding_service.generate_embedding(text)
            )

            updated += 1

            if updated % BATCH_SIZE == 0:
                db.commit()

                print(
                    f"Generated embeddings: "
                    f"{updated}/{total}"
                )

        db.commit()

        print(
            f"Embedding generation completed: "
            f"{updated}/{total}"
        )

    except Exception as exc:

        db.rollback()

        print(
            f"Embedding generation failed: {exc}"
        )

        raise

    finally:
        db.close()


if __name__ == "__main__":
    update_embeddings()