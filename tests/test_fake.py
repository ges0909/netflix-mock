from flaky import flaky


@flaky(max_runs=3)
def test_fake_put(client):
    response = client.put("/fake?status_code=400")
    assert response.status_code == 400
    data = response.json()
    assert "message" in data


@flaky(max_runs=3)
def test_fake_delete(client):
    response = client.delete("/fake?status_code=401")
    assert response.status_code == 401
    data = response.json()
    assert "message" in data
