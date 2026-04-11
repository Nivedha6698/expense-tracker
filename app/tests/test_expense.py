def get_token(client):
    client.post('/signup', json={
        "username": "user1",
        "password": "1234"
    })
    res = client.post('/login', json={
        "username": "user1",
        "password": "1234"
    })
    return res.get_json()['access_token']


def test_add_expense(client):
    token = get_token(client)

    res = client.post('/expenses',
        headers={"Authorization": f"Bearer {token}"},
        json={
            "amount": 100,
            "category": "Food",
            "notes": "Lunch"
        }
    )

    assert res.status_code == 201


def test_get_expenses(client):
    token = get_token(client)

    client.post('/expenses',
        headers={"Authorization": f"Bearer {token}"},
        json={"amount": 50}
    )

    res = client.get('/expenses',
        headers={"Authorization": f"Bearer {token}"}
    )

    assert res.status_code == 200
    assert isinstance(res.get_json(), list)

    #assert isinstance(res.get_json(), list)