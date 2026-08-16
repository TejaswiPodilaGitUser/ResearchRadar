def test_get_metrics(client):
    response = client.get(
        "/api/metrics"
    )

    assert response.status_code == 200

    data = response.json()

    assert data is not None


def test_get_api_performance_metrics(client):
    response = client.get(
        "/api/metrics/performance"
    )

    assert response.status_code == 200

    data = response.json()

    assert data is not None