from app import app


def test_dashboard_loads():
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert b"Linux Server Operations" in response.data
