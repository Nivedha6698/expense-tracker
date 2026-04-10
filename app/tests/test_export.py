from unittest.mock import patch


def get_token(client):
    client.post('/signup', json={
        "username": "user2",
        "password": "1234"
    })
    res = client.post('/login', json={
        "username": "user2",
        "password": "1234"
    })
    return res.get_json()['access_token']


@patch("app.routes.upload_csv_to_s3")
@patch("app.routes.generate_download_url")
def test_export(mock_url, mock_upload, client):
    token = get_token(client)

    # mock S3
    mock_upload.return_value = "fake-key.csv"
    mock_url.return_value = "http://fake-url.com/file.csv"

    res = client.get('/expenses/export',
        headers={"Authorization": f"Bearer {token}"}
    )

    data = res.get_json()

    assert res.status_code == 200
    assert "download_url" in data