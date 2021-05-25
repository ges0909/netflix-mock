def test_put(client):
    data = dict(
        chargingType="dsl",
        externalIdentifier1="gerrit",
        products=["Product A", "Product B"],
    )
    response = client.put(
        url="/efir/route/id",
        json=data,
    )
    assert response.status_code == 200
    data = response.json()
    assert "message" in data


def test_delete(client):
    response = client.delete(
        url="/efir/route/id",
    )
    assert response.status_code == 200
