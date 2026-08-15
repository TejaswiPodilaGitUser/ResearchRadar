import pytest


# ============================================================
# Test Data Helpers
# ============================================================

def get_existing_author_id(client) -> int:
    """
    Get an existing author ID through the API.
    """

    response = client.get(
        "/api/authors",
        params={
            "page": 1,
            "size": 1,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["results"], "Test database contains no authors."

    return data["results"][0]["author_id"]


def get_existing_author(client) -> dict:
    """
    Get one existing author from the API.
    """

    author_id = get_existing_author_id(client)

    response = client.get(
        f"/api/authors/{author_id}"
    )

    assert response.status_code == 200

    return response.json()


# ============================================================
# GET /api/authors
# ============================================================

class TestGetAuthors:

    def test_get_authors_success(self, client):
        """
        Get authors using default parameters.
        """

        response = client.get(
            "/api/authors"
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

    def test_get_authors_with_pagination(self, client):
        """
        Verify page and size parameters.
        """

        response = client.get(
            "/api/authors",
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

    def test_get_authors_second_page(self, client):
        """
        Verify pagination can retrieve another page.
        """

        response = client.get(
            "/api/authors",
            params={
                "page": 2,
                "size": 5,
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert data["page"] == 2
        assert data["page_size"] == 5

    def test_get_authors_by_name(self, client):
        """
        Search authors by name.
        """

        response = client.get(
            "/api/authors",
            params={
                "name": "John",
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert "results" in data

    def test_get_authors_no_results(self, client):
        """
        Search for an author that should not exist.
        """

        response = client.get(
            "/api/authors",
            params={
                "name": "THIS_AUTHOR_SHOULD_NOT_EXIST_123456789",
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert data["total"] == 0
        assert data["results"] == []

    def test_get_authors_invalid_page(self, client):
        """
        Page must be >= 1.
        """

        response = client.get(
            "/api/authors",
            params={
                "page": 0,
            },
        )

        assert response.status_code == 422

    def test_get_authors_invalid_size(self, client):
        """
        Size must be >= 1.
        """

        response = client.get(
            "/api/authors",
            params={
                "size": 0,
            },
        )

        assert response.status_code == 422

    def test_get_authors_size_above_maximum(self, client):
        """
        Size must not exceed configured maximum.
        """

        response = client.get(
            "/api/authors",
            params={
                "size": 10000,
            },
        )

        assert response.status_code == 422


# ============================================================
# GET /api/authors/{author_id}
# ============================================================

class TestGetAuthorById:

    def test_get_author_by_id_success(self, client):
        """
        Retrieve an existing author by ID.
        """

        author_id = get_existing_author_id(client)

        response = client.get(
            f"/api/authors/{author_id}"
        )

        assert response.status_code == 200

        data = response.json()

        assert data["author_id"] == author_id
        assert "author_name" in data

    def test_get_author_by_id_name_structure(self, client):
        """
        Verify author response structure.
        """

        data = get_existing_author(client)

        assert "author_id" in data
        assert "author_name" in data

        assert isinstance(
            data["author_id"],
            int,
        )

        assert isinstance(
            data["author_name"],
            str,
        )

    def test_get_author_by_id_not_found(self, client):
        """
        Unknown author ID should return 404.
        """

        response = client.get(
            "/api/authors/999999999"
        )

        assert response.status_code == 404

    def test_get_author_by_id_zero(self, client):
        """
        Author ID must be positive.
        """

        response = client.get(
            "/api/authors/0"
        )

        assert response.status_code in {
            404,
            422,
        }

    def test_get_author_by_id_negative(self, client):
        """
        Negative author ID should not return an author.
        """

        response = client.get(
            "/api/authors/-1"
        )

        assert response.status_code in {
            404,
            422,
        }

    def test_get_author_by_id_invalid(self, client):
        """
        Non-numeric author ID should fail validation.
        """

        response = client.get(
            "/api/authors/invalid"
        )

        assert response.status_code == 422


# ============================================================
# GET /api/authors/name
# ============================================================

class TestGetAuthorByName:

    def test_get_author_by_name_success(self, client):
        """
        Retrieve an existing author by exact name.
        """

        author = get_existing_author(client)

        author_name = author["author_name"]

        response = client.get(
            "/api/authors/name",
            params={
                "name": author_name,
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert data["author_id"] == author["author_id"]
        assert data["author_name"] == author_name

    def test_get_author_by_name_case_insensitive(self, client):
        """
        Author name lookup should be case-insensitive.
        """

        author = get_existing_author(client)

        author_name = author["author_name"]

        response = client.get(
            "/api/authors/name",
            params={
                "name": author_name.upper(),
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert data["author_id"] == author["author_id"]

    def test_get_author_by_name_with_spaces(self, client):
        """
        Leading and trailing spaces should be ignored.
        """

        author = get_existing_author(client)

        author_name = author["author_name"]

        response = client.get(
            "/api/authors/name",
            params={
                "name": f"  {author_name}  ",
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert data["author_id"] == author["author_id"]

    def test_get_author_by_name_not_found(self, client):
        """
        Unknown author name should return 404.
        """

        response = client.get(
            "/api/authors/name",
            params={
                "name": "THIS AUTHOR DOES NOT EXIST 123456789",
            },
        )

        assert response.status_code == 404

    def test_get_author_by_name_empty(self, client):
        """
        Empty author name should fail validation.
        """

        response = client.get(
            "/api/authors/name",
            params={
                "name": "",
            },
        )

        assert response.status_code == 422


# ============================================================
# GET /api/authors/collection/ids
# ============================================================

class TestGetAuthorsByIds:

    def test_get_authors_by_single_id(self, client):
        """
        Retrieve one author using the collection endpoint.
        """

        author_id = get_existing_author_id(client)

        response = client.get(
            "/api/authors/collection/ids",
            params={
                "ids": str(author_id),
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert data["requested_count"] == 1
        assert data["returned_count"] == 1
        assert len(data["results"]) == 1
        assert data["results"][0]["author_id"] == author_id

    def test_get_authors_by_multiple_ids(self, client):
        """
        Retrieve multiple authors by IDs.
        """

        response = client.get(
            "/api/authors",
            params={
                "size": 3,
            },
        )

        assert response.status_code == 200

        authors = response.json()["results"]

        if len(authors) < 2:
            pytest.skip(
                "Test database contains fewer than 2 authors."
            )

        ids = [
            authors[0]["author_id"],
            authors[1]["author_id"],
        ]

        response = client.get(
            "/api/authors/collection/ids",
            params={
                "ids": ",".join(map(str, ids)),
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert data["requested_count"] == 2
        assert data["returned_count"] == 2

        returned_ids = [
            author["author_id"]
            for author in data["results"]
        ]

        assert returned_ids == ids

    def test_get_authors_by_ids_removes_duplicates(self, client):
        """
        Duplicate IDs should be removed.
        """

        author_id = get_existing_author_id(client)

        response = client.get(
            "/api/authors/collection/ids",
            params={
                "ids": (
                    f"{author_id},"
                    f"{author_id},"
                    f"{author_id}"
                ),
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert data["requested_count"] == 1
        assert data["returned_count"] == 1
        assert len(data["results"]) == 1

    def test_get_authors_by_ids_preserves_order(self, client):
        """
        Requested ID order should be preserved.
        """

        response = client.get(
            "/api/authors",
            params={
                "size": 3,
            },
        )

        assert response.status_code == 200

        authors = response.json()["results"]

        if len(authors) < 2:
            pytest.skip(
                "Test database contains fewer than 2 authors."
            )

        ids = [
            authors[1]["author_id"],
            authors[0]["author_id"],
        ]

        response = client.get(
            "/api/authors/collection/ids",
            params={
                "ids": ",".join(map(str, ids)),
            },
        )

        assert response.status_code == 200

        returned_ids = [
            author["author_id"]
            for author in response.json()["results"]
        ]

        assert returned_ids == ids

    def test_get_authors_by_ids_missing_id(self, client):
        """
        Missing IDs should be ignored.
        """

        existing_id = get_existing_author_id(client)

        response = client.get(
            "/api/authors/collection/ids",
            params={
                "ids": f"{existing_id},999999999",
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert data["requested_count"] == 2
        assert data["returned_count"] == 1
        assert len(data["results"]) == 1
        assert data["results"][0]["author_id"] == existing_id

    def test_get_authors_by_ids_invalid_id(self, client):
        """
        Non-numeric IDs should return 400.
        """

        response = client.get(
            "/api/authors/collection/ids",
            params={
                "ids": "abc",
            },
        )

        assert response.status_code == 400

    def test_get_authors_by_ids_zero(self, client):
        """
        Zero is not a valid author ID.
        """

        response = client.get(
            "/api/authors/collection/ids",
            params={
                "ids": "0",
            },
        )

        assert response.status_code == 400

    def test_get_authors_by_ids_negative(self, client):
        """
        Negative IDs should be rejected.
        """

        response = client.get(
            "/api/authors/collection/ids",
            params={
                "ids": "-1",
            },
        )

        assert response.status_code == 400

    def test_get_authors_by_ids_empty(self, client):
        """
        Empty ID collection should fail validation.
        """

        response = client.get(
            "/api/authors/collection/ids",
            params={
                "ids": "",
            },
        )

        assert response.status_code == 422


# ============================================================
# GET /api/authors/collection/names
# ============================================================

class TestGetAuthorsByNames:

    def test_get_authors_by_single_name(self, client):
        """
        Retrieve one author by name.
        """

        author = get_existing_author(client)

        response = client.get(
            "/api/authors/collection/names",
            params={
                "names": author["author_name"],
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert data["requested_count"] == 1
        assert data["returned_count"] == 1
        assert len(data["results"]) == 1

        assert (
            data["results"][0]["author_id"]
            == author["author_id"]
        )

    def test_get_authors_by_multiple_names(self, client):
        """
        Retrieve multiple authors by names.
        """

        response = client.get(
            "/api/authors",
            params={
                "size": 3,
            },
        )

        assert response.status_code == 200

        authors = response.json()["results"]

        if len(authors) < 2:
            pytest.skip(
                "Test database contains fewer than 2 authors."
            )

        names = [
            authors[0]["author_name"],
            authors[1]["author_name"],
        ]

        response = client.get(
            "/api/authors/collection/names",
            params={
                "names": ",".join(names),
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert data["requested_count"] == 2
        assert data["returned_count"] == 2

        returned_ids = [
            author["author_id"]
            for author in data["results"]
        ]

        expected_ids = [
            authors[0]["author_id"],
            authors[1]["author_id"],
        ]

        assert returned_ids == expected_ids

    def test_get_authors_by_names_case_insensitive(self, client):
        """
        Name matching should be case-insensitive.
        """

        author = get_existing_author(client)

        response = client.get(
            "/api/authors/collection/names",
            params={
                "names": author["author_name"].upper(),
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert data["returned_count"] == 1

        assert (
            data["results"][0]["author_id"]
            == author["author_id"]
        )

    def test_get_authors_by_names_removes_duplicates(self, client):
        """
        Duplicate names should be removed case-insensitively.
        """

        author = get_existing_author(client)

        name = author["author_name"]

        response = client.get(
            "/api/authors/collection/names",
            params={
                "names": f"{name},{name},{name.upper()}",
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert data["requested_count"] == 1
        assert data["returned_count"] == 1
        assert len(data["results"]) == 1

    def test_get_authors_by_names_missing_name(self, client):
        """
        Missing author names should be ignored.
        """

        author = get_existing_author(client)

        response = client.get(
            "/api/authors/collection/names",
            params={
                "names": (
                    f"{author['author_name']},"
                    "THIS AUTHOR DOES NOT EXIST 123456789"
                ),
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert data["requested_count"] == 2
        assert data["returned_count"] == 1

        assert (
            data["results"][0]["author_id"]
            == author["author_id"]
        )

    def test_get_authors_by_names_preserves_order(self, client):
        """
        Requested name order should be preserved.
        """

        response = client.get(
            "/api/authors",
            params={
                "size": 3,
            },
        )

        assert response.status_code == 200

        authors = response.json()["results"]

        if len(authors) < 2:
            pytest.skip(
                "Test database contains fewer than 2 authors."
            )

        names = [
            authors[1]["author_name"],
            authors[0]["author_name"],
        ]

        response = client.get(
            "/api/authors/collection/names",
            params={
                "names": ",".join(names),
            },
        )

        assert response.status_code == 200

        returned_ids = [
            author["author_id"]
            for author in response.json()["results"]
        ]

        expected_ids = [
            authors[1]["author_id"],
            authors[0]["author_id"],
        ]

        assert returned_ids == expected_ids

    def test_get_authors_by_names_not_found(self, client):
        """
        Unknown author name should return an empty collection.
        """

        response = client.get(
            "/api/authors/collection/names",
            params={
                "names": (
                    "THIS AUTHOR DOES NOT EXIST "
                    "123456789"
                ),
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert data["requested_count"] == 1
        assert data["returned_count"] == 0
        assert data["results"] == []

    def test_get_authors_by_names_empty(self, client):
        """
        Empty names parameter should fail validation.
        """

        response = client.get(
            "/api/authors/collection/names",
            params={
                "names": "",
            },
        )

        assert response.status_code == 422