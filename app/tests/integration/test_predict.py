import http


def test_poster_predict(client, test_images_in_byte):
    rv = client.post('/predict', data=test_images_in_byte[0])
    assert rv.status_code == http.HTTPStatus.OK