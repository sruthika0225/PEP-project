def test_alarm_api(client):
    response = client.get("/api/tasks")
    assert response.status_code == 200
