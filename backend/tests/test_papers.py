import pytest


# ============================================================
# Test Data Helpers
# ============================================================

def get_existing_paper_id(client) -> int:
    """
    Get an existing paper ID from the database through the API.
    """

    response = client.get(
        "/api/papers",
        params={
            "page": 1,
            "size": 1,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["results"], "Test database contains no papers."

    return data["results"][0]["paper_id"]


def get_existing_paper(client) -> dict:
    """
    Get one existing paper from the API.
    """

    paper_id = get_existing_paper_id(client)

    response = client.get(
        f"/api/papers/{paper_id}"
    )

    assert response.status_code == 200

    return response.json()


# ============================================================
# GET /api/papers
# ============================================================

class TestGetPapers:

    def test_get_papers_success(self, client):
        """
        Get papers using default parameters.
        """

        response = client.get(
            "/api/papers"
        )

        assert response.status_code == 200

        data = response.json()

        assert "page" in data
        assert "page_size" in data
        assert "total" in data
        assert "results" in data

        assert isinstance(data["page"], int)
        assert isinstance(data["page_size"], int)
        assert isinstance(data["total"], int)
        assert isinstance(data["results"], list)

    def test_get_papers_with_pagination(self, client):
        """
        Verify page and size parameters.
        """

        response = client.get(
            "/api/papers",
            params={
                "page": 1,
                "size": 5,
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert data["page"] == 1
        assert data["page_size"] == 5
        assert len(data["results"]) <= 5

    def test_get_papers_second_page(self, client):
        """
        Verify pagination can retrieve another page.
        """

        response = client.get(
            "/api/papers",
            params={
                "page": 2,
                "size": 5,
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert data["page"] == 2
        assert data["page_size"] == 5

    def test_get_papers_by_keyword(self, client):
        """
        Search papers by keyword.
        """

        response = client.get(
            "/api/papers",
            params={
                "keyword": "artificial",
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert "results" in data

    def test_get_papers_by_year(self, client):
        """
        Filter papers by publication year.
        """

        response = client.get(
            "/api/papers",
            params={
                "year": 2025,
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert "results" in data

        for paper in data["results"]:
            assert paper["publication_year"] == 2025

    def test_get_papers_by_topic(self, client):
        """
        Filter papers by topic.
        """

        response = client.get(
            "/api/papers",
            params={
                "topic": "artificial intelligence",
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert "results" in data

    def test_get_papers_by_author(self, client):
        """
        Filter papers by author.
        """

        response = client.get(
            "/api/papers",
            params={
                "author": "John",
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert "results" in data

    def test_get_papers_with_multiple_filters(self, client):
        """
        Verify multiple filters can be combined.
        """

        response = client.get(
            "/api/papers",
            params={
                "keyword": "AI",
                "year": 2025,
                "topic": "artificial",
                "author": "John",
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert "results" in data
        assert "total" in data

    def test_get_papers_no_results(self, client):
        """
        Search for a value that should not exist.
        """

        response = client.get(
            "/api/papers",
            params={
                "keyword": "THIS_PAPER_SHOULD_NOT_EXIST_123456789",
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert data["total"] == 0
        assert data["results"] == []

    def test_get_papers_invalid_page(self, client):
        """
        Page must be >= 1.
        """

        response = client.get(
            "/api/papers",
            params={
                "page": 0,
            },
        )

        assert response.status_code == 422

    def test_get_papers_invalid_size(self, client):
        """
        Size must be >= 1.
        """

        response = client.get(
            "/api/papers",
            params={
                "size": 0,
            },
        )

        assert response.status_code == 422

    def test_get_papers_size_above_maximum(self, client):
        """
        Size must not exceed MAX_PAGE_SIZE.

        This assumes the configured maximum is less than 10000.
        """

        response = client.get(
            "/api/papers",
            params={
                "size": 10000,
            },
        )

        assert response.status_code == 422

    def test_get_papers_invalid_year(self, client):
        """
        Publication year outside configured range
        should fail validation.
        """

        response = client.get(
            "/api/papers",
            params={
                "year": 1800,
            },
        )

        assert response.status_code == 422


# ============================================================
# GET /api/papers/{paper_id}
# ============================================================

class TestGetPaperById:

    def test_get_paper_by_id_success(self, client):
        """
        Retrieve an existing paper by ID.
        """

        paper_id = get_existing_paper_id(client)

        response = client.get(
            f"/api/papers/{paper_id}"
        )

        assert response.status_code == 200

        data = response.json()

        assert data["paper_id"] == paper_id
        assert "paper_name" in data
        assert "abstract" in data
        assert "publication_year" in data
        assert "doi" in data
        assert "cited_by_count" in data
        assert "authors" in data
        assert "topics" in data

    def test_get_paper_by_id_authors_structure(
        self,
        client,
    ):
        """
        Verify author response structure.
        """

        data = get_existing_paper(client)

        for author in data["authors"]:
            assert "author_id" in author
            assert "author_name" in author

    def test_get_paper_by_id_topics_structure(
        self,
        client,
    ):
        """
        Verify topic response structure.
        """

        data = get_existing_paper(client)

        for topic in data["topics"]:
            assert "topic_id" in topic
            assert "topic_name" in topic

    def test_get_paper_by_id_not_found(self, client):
        """
        Unknown paper ID should return 404.
        """

        response = client.get(
            "/api/papers/999999999"
        )

        assert response.status_code == 404

    def test_get_paper_by_id_zero(self, client):
        """
        Paper ID must be positive.
        """

        response = client.get(
            "/api/papers/0"
        )

        assert response.status_code in {
            404,
            422,
        }

    def test_get_paper_by_id_negative(self, client):
        """
        Negative paper ID should not return a paper.
        """

        response = client.get(
            "/api/papers/-1"
        )

        assert response.status_code in {
            404,
            422,
        }

    def test_get_paper_by_id_invalid(self, client):
        """
        Non-numeric paper ID should fail FastAPI validation.
        """

        response = client.get(
            "/api/papers/invalid"
        )

        assert response.status_code == 422


# ============================================================
# GET /api/papers/name
# ============================================================

class TestGetPaperByName:

    def test_get_paper_by_name_success(self, client):
        """
        Retrieve an existing paper by exact title.
        """

        paper = get_existing_paper(client)

        paper_name = paper["paper_name"]

        response = client.get(
            "/api/papers/name",
            params={
                "name": paper_name,
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert data["paper_id"] == paper["paper_id"]
        assert data["paper_name"] == paper_name

    def test_get_paper_by_name_case_insensitive(
        self,
        client,
    ):
        """
        Paper name lookup should be case-insensitive.
        """

        paper = get_existing_paper(client)

        paper_name = paper["paper_name"]

        response = client.get(
            "/api/papers/name",
            params={
                "name": paper_name.upper(),
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert data["paper_id"] == paper["paper_id"]

    def test_get_paper_by_name_with_spaces(
        self,
        client,
    ):
        """
        Leading/trailing spaces should be ignored.
        """

        paper = get_existing_paper(client)

        paper_name = paper["paper_name"]

        response = client.get(
            "/api/papers/name",
            params={
                "name": f"  {paper_name}  ",
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert data["paper_id"] == paper["paper_id"]

    def test_get_paper_by_name_not_found(
        self,
        client,
    ):
        """
        Unknown paper name should return 404.
        """

        response = client.get(
            "/api/papers/name",
            params={
                "name": "THIS PAPER DOES NOT EXIST 123456789",
            },
        )

        assert response.status_code == 404

    def test_get_paper_by_name_empty(
        self,
        client,
    ):
        """
        Empty paper name should fail validation.
        """

        response = client.get(
            "/api/papers/name",
            params={
                "name": "",
            },
        )

        assert response.status_code == 422


# ============================================================
# GET /api/papers/collection/ids
# ============================================================

class TestGetPapersByIds:

    def test_get_papers_by_single_id(
        self,
        client,
    ):
        """
        Retrieve one paper using the collection endpoint.
        """

        paper_id = get_existing_paper_id(client)

        response = client.get(
            "/api/papers/collection/ids",
            params={
                "ids": str(paper_id),
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert data["requested_count"] == 1
        assert data["returned_count"] == 1
        assert len(data["results"]) == 1
        assert data["results"][0]["paper_id"] == paper_id

    def test_get_papers_by_multiple_ids(
        self,
        client,
    ):
        """
        Retrieve multiple papers by IDs.
        """

        response = client.get(
            "/api/papers",
            params={
                "size": 3,
            },
        )

        assert response.status_code == 200

        papers = response.json()["results"]

        if len(papers) < 2:
            pytest.skip(
                "Test database contains fewer than 2 papers."
            )

        ids = [
            papers[0]["paper_id"],
            papers[1]["paper_id"],
        ]

        response = client.get(
            "/api/papers/collection/ids",
            params={
                "ids": ",".join(map(str, ids)),
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert data["requested_count"] == 2
        assert data["returned_count"] == 2

        returned_ids = [
            paper["paper_id"]
            for paper in data["results"]
        ]

        assert returned_ids == ids

    def test_get_papers_by_ids_removes_duplicates(
        self,
        client,
    ):
        """
        Duplicate IDs should be removed.
        """

        paper_id = get_existing_paper_id(client)

        response = client.get(
            "/api/papers/collection/ids",
            params={
                "ids": f"{paper_id},{paper_id},{paper_id}",
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert data["requested_count"] == 1
        assert data["returned_count"] == 1
        assert len(data["results"]) == 1

    def test_get_papers_by_ids_preserves_order(
        self,
        client,
    ):
        """
        Requested ID order should be preserved.
        """

        response = client.get(
            "/api/papers",
            params={
                "size": 3,
            },
        )

        papers = response.json()["results"]

        if len(papers) < 2:
            pytest.skip(
                "Test database contains fewer than 2 papers."
            )

        ids = [
            papers[1]["paper_id"],
            papers[0]["paper_id"],
        ]

        response = client.get(
            "/api/papers/collection/ids",
            params={
                "ids": ",".join(map(str, ids)),
            },
        )

        assert response.status_code == 200

        returned_ids = [
            paper["paper_id"]
            for paper in response.json()["results"]
        ]

        assert returned_ids == ids

    def test_get_papers_by_ids_missing_id(
        self,
        client,
    ):
        """
        Missing IDs should be ignored.
        """

        existing_id = get_existing_paper_id(client)

        response = client.get(
            "/api/papers/collection/ids",
            params={
                "ids": f"{existing_id},999999999",
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert data["requested_count"] == 2
        assert data["returned_count"] == 1
        assert len(data["results"]) == 1
        assert data["results"][0]["paper_id"] == existing_id

    def test_get_papers_by_ids_invalid_id(
        self,
        client,
    ):
        """
        Non-numeric IDs should return 400.
        """

        response = client.get(
            "/api/papers/collection/ids",
            params={
                "ids": "abc",
            },
        )

        assert response.status_code == 400

    def test_get_papers_by_ids_zero(
        self,
        client,
    ):
        """
        Zero is not a valid paper ID.
        """

        response = client.get(
            "/api/papers/collection/ids",
            params={
                "ids": "0",
            },
        )

        assert response.status_code == 400

    def test_get_papers_by_ids_negative(
        self,
        client,
    ):
        """
        Negative IDs should be rejected.
        """

        response = client.get(
            "/api/papers/collection/ids",
            params={
                "ids": "-1",
            },
        )

        assert response.status_code == 400

    def test_get_papers_by_ids_empty(
        self,
        client,
    ):
        """
        Empty ID collection should fail validation.
        """

        response = client.get(
            "/api/papers/collection/ids",
            params={
                "ids": "",
            },
        )

        assert response.status_code == 422


# ============================================================
# GET /api/papers/collection/names
# ============================================================

class TestGetPapersByNames:

    def test_get_papers_by_single_name(
        self,
        client,
    ):
        """
        Retrieve one paper by name.
        """

        paper = get_existing_paper(client)

        response = client.get(
            "/api/papers/collection/names",
            params={
                "names": paper["paper_name"],
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert data["requested_count"] == 1
        assert data["returned_count"] == 1
        assert len(data["results"]) == 1
        assert (
            data["results"][0]["paper_id"]
            == paper["paper_id"]
        )

    def test_get_papers_by_multiple_names(
        self,
        client,
    ):
        """
        Retrieve multiple papers by names.
        """

        response = client.get(
            "/api/papers",
            params={
                "size": 3,
            },
        )

        papers = response.json()["results"]

        if len(papers) < 2:
            pytest.skip(
                "Test database contains fewer than 2 papers."
            )

        names = [
            papers[0]["paper_name"],
            papers[1]["paper_name"],
        ]

        response = client.get(
            "/api/papers/collection/names",
            params={
                "names": ",".join(names),
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert data["requested_count"] == 2
        assert data["returned_count"] == 2

        returned_ids = [
            paper["paper_id"]
            for paper in data["results"]
        ]

        expected_ids = [
            papers[0]["paper_id"],
            papers[1]["paper_id"],
        ]

        assert returned_ids == expected_ids

    def test_get_papers_by_names_case_insensitive(
        self,
        client,
    ):
        """
        Name matching should be case-insensitive.
        """

        paper = get_existing_paper(client)

        response = client.get(
            "/api/papers/collection/names",
            params={
                "names": paper["paper_name"].upper(),
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert data["returned_count"] == 1

        assert (
            data["results"][0]["paper_id"]
            == paper["paper_id"]
        )

    def test_get_papers_by_names_removes_duplicates(
        self,
        client,
    ):
        """
        Duplicate names should be removed
        case-insensitively.
        """

        paper = get_existing_paper(client)

        name = paper["paper_name"]

        response = client.get(
            "/api/papers/collection/names",
            params={
                "names": f"{name},{name},{name.upper()}",
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert data["requested_count"] == 1
        assert data["returned_count"] == 1
        assert len(data["results"]) == 1

    def test_get_papers_by_names_missing_name(
        self,
        client,
    ):
        """
        Missing paper names should be ignored.
        """

        paper = get_existing_paper(client)

        response = client.get(
            "/api/papers/collection/names",
            params={
                "names": (
                    f"{paper['paper_name']},"
                    "THIS PAPER DOES NOT EXIST 123456789"
                ),
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert data["requested_count"] == 2
        assert data["returned_count"] == 1

        assert (
            data["results"][0]["paper_id"]
            == paper["paper_id"]
        )

    def test_get_papers_by_names_preserves_order(
        self,
        client,
    ):
        """
        Requested name order should be preserved.
        """

        response = client.get(
            "/api/papers",
            params={
                "size": 3,
            },
        )

        papers = response.json()["results"]

        if len(papers) < 2:
            pytest.skip(
                "Test database contains fewer than 2 papers."
            )

        names = [
            papers[1]["paper_name"],
            papers[0]["paper_name"],
        ]

        response = client.get(
            "/api/papers/collection/names",
            params={
                "names": ",".join(names),
            },
        )

        assert response.status_code == 200

        returned_ids = [
            paper["paper_id"]
            for paper in response.json()["results"]
        ]

        expected_ids = [
            papers[1]["paper_id"],
            papers[0]["paper_id"],
        ]

        assert returned_ids == expected_ids

    def test_get_papers_by_names_not_found(
        self,
        client,
    ):
        """
        Unknown paper name should return an empty collection.
        """

        response = client.get(
            "/api/papers/collection/names",
            params={
                "names": "THIS PAPER DOES NOT EXIST 123456789",
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert data["requested_count"] == 1
        assert data["returned_count"] == 0
        assert data["results"] == []

    def test_get_papers_by_names_empty(
        self,
        client,
    ):
        """
        Empty names parameter should fail validation.
        """

        response = client.get(
            "/api/papers/collection/names",
            params={
                "names": "",
            },
        )

        assert response.status_code == 422