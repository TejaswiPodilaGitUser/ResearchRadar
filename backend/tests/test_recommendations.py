# ============================================================
# RECOMMENDATIONS API TESTS
# ============================================================


# ============================================================
# Trending Papers
# ============================================================

def test_get_trending_papers(client):
    response = client.get(
        "/api/recommendations/trending"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


def test_get_trending_papers_with_limit(client):
    response = client.get(
        "/api/recommendations/trending",
        params={
            "limit": 5,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) <= 5


def test_get_trending_papers_limit_one(client):
    response = client.get(
        "/api/recommendations/trending",
        params={
            "limit": 1,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) <= 1


def test_get_trending_papers_max_limit(client):
    response = client.get(
        "/api/recommendations/trending",
        params={
            "limit": 10,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) <= 10


def test_get_trending_papers_limit_zero(client):
    response = client.get(
        "/api/recommendations/trending",
        params={
            "limit": 0,
        },
    )

    assert response.status_code == 422


def test_get_trending_papers_limit_above_maximum(client):
    response = client.get(
        "/api/recommendations/trending",
        params={
            "limit": 11,
        },
    )

    assert response.status_code == 422


# ============================================================
# Emerging Topics
# ============================================================

def test_get_emerging_topics(client):
    response = client.get(
        "/api/recommendations/emerging-topics"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


def test_get_emerging_topics_with_limit(client):
    response = client.get(
        "/api/recommendations/emerging-topics",
        params={
            "limit": 5,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) <= 5


def test_get_emerging_topics_limit_one(client):
    response = client.get(
        "/api/recommendations/emerging-topics",
        params={
            "limit": 1,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) <= 1


def test_get_emerging_topics_max_limit(client):
    response = client.get(
        "/api/recommendations/emerging-topics",
        params={
            "limit": 10,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) <= 10


def test_get_emerging_topics_limit_zero(client):
    response = client.get(
        "/api/recommendations/emerging-topics",
        params={
            "limit": 0,
        },
    )

    assert response.status_code == 422


def test_get_emerging_topics_limit_above_maximum(client):
    response = client.get(
        "/api/recommendations/emerging-topics",
        params={
            "limit": 11,
        },
    )

    assert response.status_code == 422


def test_get_emerging_topics_response_fields(client):
    response = client.get(
        "/api/recommendations/emerging-topics",
        params={
            "limit": 5,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    if data:
        topic = data[0]

        assert "topic_id" in topic
        assert "topic_name" in topic
        assert "paper_count" in topic
        assert "recent_paper_count" in topic
        assert "citation_count" in topic


# ============================================================
# Top Authors
# ============================================================

def test_get_top_authors(client):
    response = client.get(
        "/api/recommendations/authors"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


def test_get_top_authors_with_limit(client):
    response = client.get(
        "/api/recommendations/authors",
        params={
            "limit": 5,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) <= 5


def test_get_top_authors_limit_one(client):
    response = client.get(
        "/api/recommendations/authors",
        params={
            "limit": 1,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) <= 1


def test_get_top_authors_max_limit(client):
    response = client.get(
        "/api/recommendations/authors",
        params={
            "limit": 10,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) <= 10


def test_get_top_authors_limit_zero(client):
    response = client.get(
        "/api/recommendations/authors",
        params={
            "limit": 0,
        },
    )

    assert response.status_code == 422


def test_get_top_authors_limit_above_maximum(client):
    response = client.get(
        "/api/recommendations/authors",
        params={
            "limit": 11,
        },
    )

    assert response.status_code == 422


def test_get_top_authors_response_fields(client):
    response = client.get(
        "/api/recommendations/authors",
        params={
            "limit": 5,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    if data:
        author = data[0]

        assert isinstance(author, dict)


# ============================================================
# Recommendation Topics
# ============================================================

def test_get_recommendation_topics(client):
    response = client.get(
        "/api/recommendations/topics"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


def test_get_recommendation_topics_with_limit(client):
    response = client.get(
        "/api/recommendations/topics",
        params={
            "limit": 5,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) <= 5


def test_get_recommendation_topics_limit_one(client):
    response = client.get(
        "/api/recommendations/topics",
        params={
            "limit": 1,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) <= 1


def test_get_recommendation_topics_max_limit(client):
    response = client.get(
        "/api/recommendations/topics",
        params={
            "limit": 10,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) <= 10


def test_get_recommendation_topics_limit_zero(client):
    response = client.get(
        "/api/recommendations/topics",
        params={
            "limit": 0,
        },
    )

    assert response.status_code == 422


def test_get_recommendation_topics_limit_above_maximum(client):
    response = client.get(
        "/api/recommendations/topics",
        params={
            "limit": 11,
        },
    )

    assert response.status_code == 422


def test_get_recommendation_topics_response_fields(client):
    response = client.get(
        "/api/recommendations/topics",
        params={
            "limit": 5,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    if data:
        topic = data[0]

        assert "topic_id" in topic
        assert "topic_name" in topic
        assert "paper_count" in topic


# ============================================================
# Papers By Topic
# ============================================================

def test_get_papers_by_topic(client):
    response = client.get(
        "/api/recommendations/topics/1/papers",
        params={
            "page": 1,
            "limit": 10,
        },
    )

    assert response.status_code in (
        200,
        404,
    )


def test_get_papers_by_topic_page_one(client):
    response = client.get(
        "/api/recommendations/topics/1/papers",
        params={
            "page": 1,
            "limit": 5,
        },
    )

    assert response.status_code in (
        200,
        404,
    )

    if response.status_code == 200:
        data = response.json()

        assert isinstance(data, dict)


def test_get_papers_by_topic_second_page(client):
    response = client.get(
        "/api/recommendations/topics/1/papers",
        params={
            "page": 2,
            "limit": 5,
        },
    )

    assert response.status_code in (
        200,
        404,
    )


def test_get_papers_by_nonexistent_topic(client):
    response = client.get(
        "/api/recommendations/topics/999999999/papers",
        params={
            "page": 1,
            "limit": 10,
        },
    )

    assert response.status_code == 404


def test_get_papers_by_topic_page_zero(client):
    response = client.get(
        "/api/recommendations/topics/1/papers",
        params={
            "page": 0,
            "limit": 10,
        },
    )

    assert response.status_code == 422


def test_get_papers_by_topic_limit_zero(client):
    response = client.get(
        "/api/recommendations/topics/1/papers",
        params={
            "page": 1,
            "limit": 0,
        },
    )

    assert response.status_code == 422


def test_get_papers_by_topic_limit_above_maximum(client):
    response = client.get(
        "/api/recommendations/topics/1/papers",
        params={
            "page": 1,
            "limit": 11,
        },
    )

    assert response.status_code == 422


def test_get_papers_by_topic_negative_page(client):
    response = client.get(
        "/api/recommendations/topics/1/papers",
        params={
            "page": -1,
            "limit": 10,
        },
    )

    assert response.status_code == 422


def test_get_papers_by_topic_invalid_id(client):
    response = client.get(
        "/api/recommendations/topics/abc/papers",
        params={
            "page": 1,
            "limit": 10,
        },
    )

    assert response.status_code == 422


# ============================================================
# Papers By Author
# ============================================================

def test_get_papers_by_author(client):
    response = client.get(
        "/api/recommendations/authors/1/papers",
        params={
            "page": 1,
            "limit": 10,
        },
    )

    assert response.status_code in (
        200,
        404,
    )


def test_get_papers_by_author_page_one(client):
    response = client.get(
        "/api/recommendations/authors/1/papers",
        params={
            "page": 1,
            "limit": 5,
        },
    )

    assert response.status_code in (
        200,
        404,
    )

    if response.status_code == 200:
        data = response.json()

        assert isinstance(data, dict)

        assert "author_id" in data
        assert "author_name" in data
        assert "page" in data
        assert "limit" in data
        assert "total" in data
        assert "total_pages" in data
        assert "has_previous" in data
        assert "has_next" in data
        assert "results" in data

        assert isinstance(
            data["results"],
            list,
        )


def test_get_papers_by_author_second_page(client):
    response = client.get(
        "/api/recommendations/authors/1/papers",
        params={
            "page": 2,
            "limit": 5,
        },
    )

    assert response.status_code in (
        200,
        404,
    )


def test_get_papers_by_nonexistent_author(client):
    response = client.get(
        "/api/recommendations/authors/999999999/papers",
        params={
            "page": 1,
            "limit": 10,
        },
    )

    assert response.status_code == 404


def test_get_papers_by_author_page_zero(client):
    response = client.get(
        "/api/recommendations/authors/1/papers",
        params={
            "page": 0,
            "limit": 10,
        },
    )

    assert response.status_code == 422


def test_get_papers_by_author_negative_page(client):
    response = client.get(
        "/api/recommendations/authors/1/papers",
        params={
            "page": -1,
            "limit": 10,
        },
    )

    assert response.status_code == 422


def test_get_papers_by_author_limit_zero(client):
    response = client.get(
        "/api/recommendations/authors/1/papers",
        params={
            "page": 1,
            "limit": 0,
        },
    )

    assert response.status_code == 422


def test_get_papers_by_author_limit_above_maximum(client):
    response = client.get(
        "/api/recommendations/authors/1/papers",
        params={
            "page": 1,
            "limit": 11,
        },
    )

    assert response.status_code == 422


def test_get_papers_by_author_invalid_id(client):
    response = client.get(
        "/api/recommendations/authors/abc/papers",
        params={
            "page": 1,
            "limit": 10,
        },
    )

    assert response.status_code == 422


def test_author_papers_pagination_values(client):
    response = client.get(
        "/api/recommendations/authors/1/papers",
        params={
            "page": 1,
            "limit": 5,
        },
    )

    if response.status_code == 200:
        data = response.json()

        assert data["page"] == 1
        assert data["limit"] == 5
        assert data["total"] >= 0
        assert data["total_pages"] >= 0

        assert isinstance(
            data["has_previous"],
            bool,
        )

        assert isinstance(
            data["has_next"],
            bool,
        )


def test_author_papers_result_fields(client):
    response = client.get(
        "/api/recommendations/authors/1/papers",
        params={
            "page": 1,
            "limit": 10,
        },
    )

    if response.status_code == 200:

        data = response.json()

        if data["results"]:

            paper = data["results"][0]

            assert "id" in paper
            assert "title" in paper
            assert "publication_year" in paper
            assert "doi" in paper
            assert "cited_by_count" in paper

            assert "embedding" not in paper


# ============================================================
# Similar Papers
# ============================================================

def test_get_similar_papers(client):
    response = client.get(
        "/api/recommendations/papers/1/similar",
        params={
            "limit": 5,
        },
    )

    assert response.status_code in (
        200,
        404,
    )


def test_get_similar_papers_with_limit(client):
    response = client.get(
        "/api/recommendations/papers/1/similar",
        params={
            "limit": 5,
        },
    )

    assert response.status_code in (
        200,
        404,
    )

    if response.status_code == 200:

        data = response.json()

        assert isinstance(data, list)
        assert len(data) <= 5


def test_get_similar_papers_limit_one(client):
    response = client.get(
        "/api/recommendations/papers/1/similar",
        params={
            "limit": 1,
        },
    )

    assert response.status_code in (
        200,
        404,
    )

    if response.status_code == 200:

        data = response.json()

        assert isinstance(data, list)
        assert len(data) <= 1


def test_get_similar_papers_max_limit(client):
    response = client.get(
        "/api/recommendations/papers/1/similar",
        params={
            "limit": 10,
        },
    )

    assert response.status_code in (
        200,
        404,
    )

    if response.status_code == 200:

        data = response.json()

        assert isinstance(data, list)
        assert len(data) <= 10


def test_get_similar_papers_nonexistent_paper(client):
    response = client.get(
        "/api/recommendations/papers/999999999/similar",
        params={
            "limit": 5,
        },
    )

    assert response.status_code == 404


def test_get_similar_papers_limit_zero(client):
    response = client.get(
        "/api/recommendations/papers/1/similar",
        params={
            "limit": 0,
        },
    )

    assert response.status_code == 422


def test_get_similar_papers_limit_above_maximum(client):
    response = client.get(
        "/api/recommendations/papers/1/similar",
        params={
            "limit": 11,
        },
    )

    assert response.status_code == 422


def test_get_similar_papers_invalid_paper_id(client):
    response = client.get(
        "/api/recommendations/papers/abc/similar",
        params={
            "limit": 5,
        },
    )

    assert response.status_code == 422


def test_get_similar_papers_response_fields(client):
    response = client.get(
        "/api/recommendations/papers/1/similar",
        params={
            "limit": 5,
        },
    )

    if response.status_code == 200:

        data = response.json()

        assert isinstance(data, list)

        for paper in data:

            assert "id" in paper
            assert "title" in paper
            assert "publication_year" in paper
            assert "doi" in paper
            assert "cited_by_count" in paper

            assert "embedding" not in paper


def test_get_similar_papers_excludes_source_paper(client):
    paper_id = 1

    response = client.get(
        f"/api/recommendations/papers/{paper_id}/similar",
        params={
            "limit": 10,
        },
    )

    if response.status_code == 200:

        data = response.json()

        paper_ids = [
            paper["id"]
            for paper in data
        ]

        assert paper_id not in paper_ids


# ============================================================
# General Recommendation Validation
# ============================================================

def test_trending_missing_limit_uses_default(client):
    response = client.get(
        "/api/recommendations/trending"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) <= 10


def test_emerging_topics_missing_limit_uses_default(client):
    response = client.get(
        "/api/recommendations/emerging-topics"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) <= 10


def test_top_authors_missing_limit_uses_default(client):
    response = client.get(
        "/api/recommendations/authors"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) <= 10


def test_recommendation_topics_missing_limit_uses_default(client):
    response = client.get(
        "/api/recommendations/topics"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) <= 10