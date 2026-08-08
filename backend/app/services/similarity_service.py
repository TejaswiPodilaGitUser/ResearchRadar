from sqlalchemy.orm import Session

from app.models.paper import Paper



def find_similar_papers(
        db: Session,
        paper_id: int,
        limit: int = 5
):

    """
    Find similar papers using vector similarity
    """


    paper = (
        db.query(Paper)
        .filter(
            Paper.id == paper_id
        )
        .first()
    )


    if not paper:

        return []



    if not paper.embedding:

        return []



    similar = (

        db.query(
            Paper
        )

        .filter(
            Paper.id != paper_id
        )

        .order_by(

            Paper.embedding.cosine_distance(
                paper.embedding
            )

        )

        .limit(limit)

        .all()
    )


    return similar