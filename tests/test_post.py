




def test_get_all_post(authorize_client,test_posts):
    res = authorize_client.get("/posts/")
    print(res.json())
    assert res.status_code == 401