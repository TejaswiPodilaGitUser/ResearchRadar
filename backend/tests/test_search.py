# ============================================================
# SEARCH API TESTS
# ============================================================


# ============================================================
# Semantic Search
# ============================================================

def test_search_papers(client):
    response = client.get(
        "/api/search",
        params={
            "q": "artificial intelligence",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


def test_search_papers_with_limit(client):
    response = client.get(
        "/api/search",
        params={
            "q": "artificial intelligence",
            "limit": 10,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    assert len(data) <= 10


def test_search_papers_returns_paper_fields(client):
    response = client.get(
        "/api/search",
        params={
            "q": "artificial intelligence",
            "limit": 5,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    if data:
        paper = data[0]

        assert "paper_id" in paper
        assert "paper_name" in paper
        assert "publication_year" in paper
        assert "cited_by_count" in paper


def test_search_papers_empty_query(client):
    response = client.get(
        "/api/search",
        params={
            "q": "",
        },
    )

    assert response.status_code == 422


def test_search_papers_missing_query(client):
    response = client.get(
        "/api/search",
    )

    assert response.status_code == 422


def test_search_papers_limit(client):
    response = client.get(
        "/api/search",
        params={
            "q": "machine learning",
            "limit": 5,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    assert len(data) <= 5


# ============================================================
# Hybrid Search
# ============================================================

def test_hybrid_search_papers(client):
    response = client.get(
        "/api/search/hybrid",
        params={
            "q": "artificial intelligence",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


def test_hybrid_search_with_limit(client):
    response = client.get(
        "/api/search/hybrid",
        params={
            "q": "natural language processing",
            "limit": 10,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    assert len(data) <= 10


def test_hybrid_search_returns_paper_fields(client):
    response = client.get(
        "/api/search/hybrid",
        params={
            "q": "natural language processing",
            "limit": 5,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    if data:
        paper = data[0]

        assert "paper_id" in paper
        assert "paper_name" in paper
        assert "publication_year" in paper
        assert "cited_by_count" in paper


def test_hybrid_search_empty_query(client):
    response = client.get(
        "/api/search/hybrid",
        params={
            "q": "",
        },
    )

    assert response.status_code == 422


def test_hybrid_search_missing_query(client):
    response = client.get(
        "/api/search/hybrid",
    )

    assert response.status_code == 422


def test_hybrid_search_limit(client):
    response = client.get(
        "/api/search/hybrid",
        params={
            "q": "machine learning",
            "limit": 5,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    assert len(data) <= 5


# ============================================================
# Search Query Validation
# ============================================================

def test_search_query_too_short(client):
    response = client.get(
        "/api/search",
        params={
            "q": "a",
        },
    )

    assert response.status_code == 422


def test_hybrid_search_query_too_short(client):
    response = client.get(
        "/api/search/hybrid",
        params={
            "q": "a",
        },
    )

    assert response.status_code == 422


def test_search_limit_zero(client):
    response = client.get(
        "/api/search",
        params={
            "q": "artificial intelligence",
            "limit": 0,
        },
    )

    assert response.status_code == 422


def test_hybrid_search_limit_zero(client):
    response = client.get(
        "/api/search/hybrid",
        params={
            "q": "artificial intelligence",
            "limit": 0,
        },
    )

    assert response.status_code == 422