from ferry import create_app


def test_config():
    assert not create_app().testing
    assert create_app({"TESTING": True}).testing


def test_message(client):
    response = client.get("/yasen")
    assert response.data == b"Yasen."
