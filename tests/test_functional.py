def test_public(testapp):
    res = testapp.get('/public', status=200)
    assert 'available_for' in res.json_body


def test_notfound(testapp):
    res = testapp.get('/badurl', status=404)
    assert res.status_code == 404
