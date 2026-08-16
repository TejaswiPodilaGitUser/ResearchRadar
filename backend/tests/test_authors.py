# ============================================================
# AUTHORS API TESTS
# ============================================================

import pytest


# ============================================================
# GET /api/authors
# ============================================================


def test_get_authors(client):
    response = client.get(
        "/api/authors"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, dict)

    assert "page" in data
    assert "page_size" in data
    assert "total" in data
    assert "results" in data

    assert isinstance(data["page"], int)
    assert isinstance(data["page_size"], int)
    assert isinstance(data["total"], int)
    assert isinstance(data["results"], list)


def test_get_authors_with_pagination(client):
    response = client.get(
        "/api/authors",
        params={
            "page": 1,
            "size": 10,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["page"] == 1
    assert data["page_size"] == 10

    assert len(data["results"]) <= 10


def test_get_authors_second_page(client):
    response = client.get(
        "/api/authors",
        params={
            "page": 2,
            "size": 10,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["page"] == 2
    assert data["page_size"] == 10

    assert len(data["results"]) <= 10


def test_get_authors_with_keyword(client):
    response = client.get(
        "/api/authors",
        params={
            "keyword": "Ford",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, dict)
    assert "results" in data
    assert isinstance(data["results"], list)


def test_get_authors_with_author_id_keyword(client):
    response = client.get(
        "/api/authors",
        params={
            "keyword": "2208",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, dict)
    assert "results" in data
    assert isinstance(data["results"], list)


def test_get_authors_keyword_not_found(client):
    response = client.get(
        "/api/authors",
        params={
            "keyword": "DefinitelyUnknownAuthor123456",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, dict)
    assert isinstance(data["results"], list)

    assert len(data["results"]) == 0


def test_get_authors_invalid_page(client):
    response = client.get(
        "/api/authors",
        params={
            "page": 0,
        },
    )

    assert response.status_code == 422


def test_get_authors_negative_page(client):
    response = client.get(
        "/api/authors",
        params={
            "page": -1,
        },
    )

    assert response.status_code == 422


def test_get_authors_invalid_size_zero(client):
    response = client.get(
        "/api/authors",
        params={
            "size": 0,
        },
    )

    assert response.status_code == 422


def test_get_authors_invalid_size_too_large(client):
    response = client.get(
        "/api/authors",
        params={
            "size": 1000,
        },
    )

    assert response.status_code == 422


# ============================================================
# GET /api/authors/{author_id}
# ============================================================


def test_get_author_by_id(client):
    response = client.get(
        "/api/authors/2208"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, dict)

    assert "author_id" in data
    assert "author_name" in data

    assert data["author_id"] == 2208


def test_get_author_by_existing_id_has_papers_field(client):
    response = client.get(
        "/api/authors/2208"
    )

    assert response.status_code == 200

    data = response.json()

    assert "papers" in data

    assert isinstance(
        data["papers"],
        list,
    )


def test_get_author_by_nonexistent_id(client):
    response = client.get(
        "/api/authors/999999999"
    )

    assert response.status_code == 404


def test_get_author_by_zero_id(client):
    response = client.get(
        "/api/authors/0"
    )

    assert response.status_code == 404


def test_get_author_by_negative_id(client):
    response = client.get(
        "/api/authors/-1"
    )

    assert response.status_code == 404


def test_get_author_by_invalid_id(client):
    response = client.get(
        "/api/authors/abc"
    )

    assert response.status_code == 422


# ============================================================
# GET /api/authors/name
# ============================================================


def test_get_author_by_name(client):
    response = client.get(
        "/api/authors/name",
        params={
            "name": "A Ford",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, dict)

    assert "author_id" in data
    assert "author_name" in data

    assert data["author_name"] == "A Ford"


def test_get_author_by_name_case_insensitive(client):
    response = client.get(
        "/api/authors/name",
        params={
            "name": "a ford",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "author_id" in data
    assert "author_name" in data

    assert data["author_name"] == "A Ford"


def test_get_author_by_name_with_leading_spaces(client):
    response = client.get(
        "/api/authors/name",
        params={
            "name": "  A Ford",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["author_name"] == "A Ford"


def test_get_author_by_name_with_trailing_spaces(client):
    response = client.get(
        "/api/authors/name",
        params={
            "name": "A Ford  ",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["author_name"] == "A Ford"


def test_get_author_by_name_with_leading_and_trailing_spaces(client):
    response = client.get(
        "/api/authors/name",
        params={
            "name": "  A Ford  ",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["author_name"] == "A Ford"


def test_get_author_by_name_unicode(client):
    response = client.get(
        "/api/authors/name",
        params={
            "name": "Μαρία Ανδρέου",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["author_name"] == "Μαρία Ανδρέου"


def test_get_author_by_name_unicode_japanese(client):
    response = client.get(
        "/api/authors/name",
        params={
            "name": "裕二 池谷",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["author_name"] == "裕二 池谷"


def test_get_author_by_name_missing_name(client):
    response = client.get(
        "/api/authors/name"
    )

    assert response.status_code == 422


def test_get_author_by_name_empty(client):
    response = client.get(
        "/api/authors/name",
        params={
            "name": "",
        },
    )

    assert response.status_code == 422


def test_get_author_by_name_not_found(client):
    response = client.get(
        "/api/authors/name",
        params={
            "name": "This Author Definitely Does Not Exist",
        },
    )

    assert response.status_code == 404


# ============================================================
# GET /api/authors/multiple/ids
# ============================================================


def test_get_multiple_authors_by_single_id(client):
    """
    A single ID is not a multiple-author request.

    The current router explicitly raises ValueError.
    TestClient re-raises that exception.
    """

    with pytest.raises(
        ValueError,
        match="At least two author IDs are required",
    ):
        client.get(
            "/api/authors/multiple/ids",
            params={
                "author_ids": "2208",
            },
        )


def test_get_multiple_authors_by_ids(client):
    response = client.get(
        "/api/authors/multiple/ids",
        params={
            "author_ids": "2208,1561",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, dict)

    assert "authors" in data

    assert isinstance(
        data["authors"],
        list,
    )


def test_get_multiple_authors_duplicate_ids(client):
    response = client.get(
        "/api/authors/multiple/ids",
        params={
            "author_ids": "2208,2208,1561",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "authors" in data

    assert isinstance(
        data["authors"],
        list,
    )


def test_get_multiple_authors_ids_preserve_order(client):
    response = client.get(
        "/api/authors/multiple/ids",
        params={
            "author_ids": "2208,1561",
        },
    )

    assert response.status_code == 200

    data = response.json()

    authors = data["authors"]

    assert isinstance(
        authors,
        list,
    )

    if len(authors) >= 2:
        assert authors[0]["author_id"] == 2208
        assert authors[1]["author_id"] == 1561


def test_get_multiple_authors_ids_invalid_values(client):
    """
    The current router explicitly raises ValueError
    when IDs are not integers.
    """

    with pytest.raises(
        ValueError,
        match="author_ids must contain only",
    ):
        client.get(
            "/api/authors/multiple/ids",
            params={
                "author_ids": "abc,xyz",
            },
        )


def test_get_multiple_authors_ids_mixed_invalid_values(client):
    """
    The current router explicitly raises ValueError
    when any ID is invalid.
    """

    with pytest.raises(
        ValueError,
        match="author_ids must contain only",
    ):
        client.get(
            "/api/authors/multiple/ids",
            params={
                "author_ids": "2208,abc",
            },
        )


def test_get_multiple_authors_ids_missing_parameter(client):
    response = client.get(
        "/api/authors/multiple/ids"
    )

    assert response.status_code == 422


def test_get_multiple_authors_ids_empty(client):
    response = client.get(
        "/api/authors/multiple/ids",
        params={
            "author_ids": "",
        },
    )

    assert response.status_code == 422


def test_get_multiple_authors_ids_whitespace(client):
    response = client.get(
        "/api/authors/multiple/ids",
        params={
            "author_ids": " 2208 , 1561 ",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "authors" in data

    assert isinstance(
        data["authors"],
        list,
    )


# ============================================================
# GET /api/authors/multiple/names
# ============================================================


def test_get_multiple_authors_by_single_name(client):
    """
    A single name is not a multiple-author request.

    The current router explicitly raises ValueError.
    """

    with pytest.raises(
        ValueError,
        match="At least two author names are required",
    ):
        client.get(
            "/api/authors/multiple/names",
            params={
                "author_names": "A Ford",
            },
        )


def test_get_multiple_authors_by_names(client):
    response = client.get(
        "/api/authors/multiple/names",
        params={
            "author_names": "A Ford,A. H. Alamoodi",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, dict)

    assert "authors" in data

    assert isinstance(
        data["authors"],
        list,
    )


def test_get_multiple_authors_names_with_spaces(client):
    response = client.get(
        "/api/authors/multiple/names",
        params={
            "author_names": (
                "  A Ford  ,  A. H. Alamoodi  "
            ),
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "authors" in data

    assert isinstance(
        data["authors"],
        list,
    )


def test_get_multiple_authors_duplicate_names(client):
    """
    Duplicate names are still two supplied names.

    Therefore the router should not reject them because
    of the minimum-count validation.
    """

    response = client.get(
        "/api/authors/multiple/names",
        params={
            "author_names": "A Ford,A Ford",
        },
    )

    assert response.status_code in (
        200,
        404,
    )


def test_get_multiple_authors_names_preserve_order(client):
    response = client.get(
        "/api/authors/multiple/names",
        params={
            "author_names": "A Ford,A. H. Alamoodi",
        },
    )

    assert response.status_code == 200

    data = response.json()

    authors = data["authors"]

    assert isinstance(
        authors,
        list,
    )

    if len(authors) >= 2:
        assert authors[0]["author_name"] == "A Ford"
        assert (
            authors[1]["author_name"]
            == "A. H. Alamoodi"
        )


def test_get_multiple_authors_names_case_insensitive(client):
    response = client.get(
        "/api/authors/multiple/names",
        params={
            "author_names": "a ford,a. h. alamoodi",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "authors" in data

    assert isinstance(
        data["authors"],
        list,
    )


def test_get_multiple_authors_names_missing_parameter(client):
    response = client.get(
        "/api/authors/multiple/names"
    )

    assert response.status_code == 422


def test_get_multiple_authors_names_empty(client):
    response = client.get(
        "/api/authors/multiple/names",
        params={
            "author_names": "",
        },
    )

    assert response.status_code == 422


def test_get_multiple_authors_names_not_found(client):
    response = client.get(
        "/api/authors/multiple/names",
        params={
            "author_names": (
                "Author Definitely Does Not Exist,"
                "Another Fake Author"
            ),
        },
    )

    assert response.status_code == 404


def test_get_multiple_authors_names_unicode(client):
    response = client.get(
        "/api/authors/multiple/names",
        params={
            "author_names": (
                "Μαρία Ανδρέου,"
                "裕二 池谷"
            ),
        },
    )

    assert response.status_code in (
        200,
        404,
    )


def test_get_multiple_authors_names_apostrophe(client):
    response = client.get(
        "/api/authors/multiple/names",
        params={
            "author_names": (
                "O'Connor,"
                "Smith-Jones"
            ),
        },
    )

    assert response.status_code in (
        200,
        404,
    )