BASE_URL = "/weather"


def test_weather(client):
    response = client.get(
        url=f"{BASE_URL}?city=berlin",
    )
    assert response.status_code == 200
    data = response.json()
    assert data["city"] == "berlin"
    assert "bring_umbrella" in data
    assert "temp" in data
