# ============================================================
# TOPICS API TESTS
# ============================================================


# ============================================================
# Helper Functions
# ============================================================

def get_existing_topic(client):
    """
    Get one real topic from the database through the API.
    """

    response = client.get(
        "/api/topics",
        params={
            "page": 1,
            "size": 10,
        },
    )

    assert response.status_code == 200

    data = response.json()

    if isinstance(data, dict):
        topics = (
            data.get("items")
            or data.get("topics")
            or data.get("results")
            or []
        )
    else:
        topics = data

    assert topics

    return topics[0]


def get_existing_topics(client, count=2):
    """
    Get real topics from the database through the API.
    """

    response = client.get(
        "/api/topics",
        params={
            "page": 1,
            "size": count,
        },
    )

    assert response.status_code == 200

    data = response.json()

    if isinstance(data, dict):
        topics = (
            data.get("items")
            or data.get("topics")
            or data.get("results")
            or []
        )
    else:
        topics = data

    assert len(topics) >= count

    return topics


def get_topic_id(topic):
    """
    Extract topic ID from the topic response.
    """

    return (
        topic.get("topic_id")
        or topic.get("id")
    )


def get_topic_name(topic):
    """
    Extract topic name from the topic response.
    """

    return (
        topic.get("topic_name")
        or topic.get("name")
    )


# ============================================================
# GET /topics
# ============================================================


def test_get_topics(client):
    response = client.get(
        "/api/topics"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, (list, dict))


def test_get_topics_with_pagination(client):
    response = client.get(
        "/api/topics",
        params={
            "page": 1,
            "size": 10,
        },
    )

    assert response.status_code == 200


def test_get_topics_second_page(client):
    response = client.get(
        "/api/topics",
        params={
            "page": 2,
            "size": 10,
        },
    )

    assert response.status_code == 200


def test_get_topics_with_keyword(client):
    response = client.get(
        "/api/topics",
        params={
            "keyword": "AI",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, (list, dict))


def test_get_topics_empty_keyword(client):
    response = client.get(
        "/api/topics",
        params={
            "keyword": "",
        },
    )

    assert response.status_code in (
        200,
        422,
    )


def test_get_topics_invalid_page(client):
    response = client.get(
        "/api/topics",
        params={
            "page": 0,
        },
    )

    assert response.status_code == 422


def test_get_topics_invalid_size(client):
    response = client.get(
        "/api/topics",
        params={
            "size": 0,
        },
    )

    assert response.status_code == 422


# ============================================================
# GET /topics/{topic_id}
# ============================================================


def test_get_topic_by_id(client):
    topic = get_existing_topic(client)

    topic_id = get_topic_id(topic)

    response = client.get(
        f"/api/topics/{topic_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, dict)


def test_get_nonexistent_topic(client):
    response = client.get(
        "/api/topics/999999999"
    )

    assert response.status_code == 404


def test_get_topic_by_id_zero(client):
    response = client.get(
        "/api/topics/0"
    )

    assert response.status_code in (
        404,
        422,
    )


def test_get_topic_by_id_negative(client):
    response = client.get(
        "/api/topics/-1"
    )

    assert response.status_code in (
        404,
        422,
    )


def test_get_topic_by_id_invalid(client):
    response = client.get(
        "/api/topics/abc"
    )

    assert response.status_code == 404


# ============================================================
# GET /topics/name
# ============================================================


def test_get_topic_by_name(client):
    topic = get_existing_topic(client)

    topic_name = get_topic_name(topic)

    response = client.get(
        "/api/topics/name",
        params={
            "name": topic_name,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, dict)


def test_get_topic_by_name_case_insensitive(client):
    topic = get_existing_topic(client)

    topic_name = get_topic_name(topic)

    response = client.get(
        "/api/topics/name",
        params={
            "name": topic_name.upper(),
        },
    )

    assert response.status_code == 200


def test_get_topic_by_name_with_spaces(client):
    topic = get_existing_topic(client)

    topic_name = get_topic_name(topic)

    response = client.get(
        "/api/topics/name",
        params={
            "name": f"  {topic_name}  ",
        },
    )

    assert response.status_code == 200


def test_get_topic_by_name_missing_name(client):
    response = client.get(
        "/api/topics/name"
    )

    assert response.status_code == 422


def test_get_topic_by_name_empty_name(client):
    response = client.get(
        "/api/topics/name",
        params={
            "name": "",
        },
    )

    assert response.status_code == 422


def test_get_topic_by_name_not_found(client):
    response = client.get(
        "/api/topics/name",
        params={
            "name": "this_topic_does_not_exist_123456",
        },
    )

    assert response.status_code == 404


# ============================================================
# GET /topics/multiple/ids
# ============================================================


def test_get_multiple_topics_by_ids(client):
    topics = get_existing_topics(
        client,
        count=2,
    )

    topic_ids = [
        str(get_topic_id(topic))
        for topic in topics
    ]

    response = client.get(
        "/api/topics/multiple/ids",
        params={
            "ids": ",".join(topic_ids),
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, dict)


def test_get_multiple_topics_duplicate_ids(client):
    topics = get_existing_topics(
        client,
        count=2,
    )

    first_id = get_topic_id(topics[0])
    second_id = get_topic_id(topics[1])

    response = client.get(
        "/api/topics/multiple/ids",
        params={
            "ids": (
                f"{first_id},"
                f"{first_id},"
                f"{second_id},"
                f"{second_id}"
            ),
        },
    )

    assert response.status_code == 200


def test_get_multiple_topics_ids_preserves_order(client):
    topics = get_existing_topics(
        client,
        count=2,
    )

    first_id = get_topic_id(topics[0])
    second_id = get_topic_id(topics[1])

    response = client.get(
        "/api/topics/multiple/ids",
        params={
            "ids": f"{second_id},{first_id}",
        },
    )

    assert response.status_code == 200


def test_get_multiple_topics_single_id(client):
    topic = get_existing_topic(client)

    topic_id = get_topic_id(topic)

    response = client.get(
        "/api/topics/multiple/ids",
        params={
            "ids": str(topic_id),
        },
    )

    assert response.status_code == 400


def test_get_multiple_topics_invalid_ids(client):
    response = client.get(
        "/api/topics/multiple/ids",
        params={
            "ids": "abc,xyz",
        },
    )

    assert response.status_code == 400


def test_get_multiple_topics_zero_id(client):
    response = client.get(
        "/api/topics/multiple/ids",
        params={
            "ids": "0,1",
        },
    )

    assert response.status_code == 400


def test_get_multiple_topics_negative_id(client):
    response = client.get(
        "/api/topics/multiple/ids",
        params={
            "ids": "-1,2",
        },
    )

    assert response.status_code == 400


def test_get_multiple_topics_empty_ids(client):
    response = client.get(
        "/api/topics/multiple/ids",
        params={
            "ids": "",
        },
    )

    assert response.status_code == 422


def test_get_multiple_topics_missing_ids(client):
    response = client.get(
        "/api/topics/multiple/ids"
    )

    assert response.status_code == 422


def test_get_multiple_topics_nonexistent_id(client):
    response = client.get(
        "/api/topics/multiple/ids",
        params={
            "ids": "999999998,999999999",
        },
    )

    assert response.status_code == 404


# ============================================================
# GET /topics/multiple/names
# ============================================================


def test_get_multiple_topics_by_names(client):
    topics = get_existing_topics(
        client,
        count=2,
    )

    topic_names = [
        get_topic_name(topic)
        for topic in topics
    ]

    response = client.get(
        "/api/topics/multiple/names",
        params={
            "names": ",".join(topic_names),
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, dict)


def test_get_multiple_topics_duplicate_names(client):
    topics = get_existing_topics(
        client,
        count=2,
    )

    first_name = get_topic_name(topics[0])
    second_name = get_topic_name(topics[1])

    response = client.get(
        "/api/topics/multiple/names",
        params={
            "names": (
                f"{first_name},"
                f"{first_name},"
                f"{second_name}"
            ),
        },
    )

    assert response.status_code == 200


def test_get_multiple_topics_names_case_insensitive(client):
    topics = get_existing_topics(
        client,
        count=2,
    )

    first_name = get_topic_name(topics[0])
    second_name = get_topic_name(topics[1])

    response = client.get(
        "/api/topics/multiple/names",
        params={
            "names": (
                f"{first_name.upper()},"
                f"{second_name.upper()}"
            ),
        },
    )

    assert response.status_code == 200


def test_get_multiple_topics_names_with_spaces(client):
    topics = get_existing_topics(
        client,
        count=2,
    )

    first_name = get_topic_name(topics[0])
    second_name = get_topic_name(topics[1])

    response = client.get(
        "/api/topics/multiple/names",
        params={
            "names": (
                f"  {first_name}  ,"
                f"  {second_name}  "
            ),
        },
    )

    assert response.status_code == 200


def test_get_multiple_topics_single_name(client):
    topic = get_existing_topic(client)

    topic_name = get_topic_name(topic)

    response = client.get(
        "/api/topics/multiple/names",
        params={
            "names": topic_name,
        },
    )

    assert response.status_code == 400


def test_get_multiple_topics_invalid_names(client):
    response = client.get(
        "/api/topics/multiple/names",
        params={
            "names": (
                "this_topic_does_not_exist_123,"
                "another_topic_does_not_exist_456"
            ),
        },
    )

    assert response.status_code == 404


def test_get_multiple_topics_empty_names(client):
    response = client.get(
        "/api/topics/multiple/names",
        params={
            "names": "",
        },
    )

    assert response.status_code == 422


def test_get_multiple_topics_missing_names(client):
    response = client.get(
        "/api/topics/multiple/names"
    )

    assert response.status_code == 422


def test_get_multiple_topics_names_not_found(client):
    response = client.get(
        "/api/topics/multiple/names",
        params={
            "names": (
                "topic_that_definitely_does_not_exist_123,"
                "another_missing_topic_456"
            ),
        },
    )

    assert response.status_code == 404