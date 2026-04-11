def test_signup(client):
    res = client.post('/signup', json={
        "username": "testuser",
        "password": "1234"
    })
    assert res.status_code == 201


def test_login(client):
    client.post('/signup', json={
        "username": "testuser",
        "password": "1234"
    })

    res = client.post('/login', json={
        "username": "testuser",
        "password": "1234"
    })

    data = res.get_json()

    assert res.status_code == 200
    assert "access_token" in data