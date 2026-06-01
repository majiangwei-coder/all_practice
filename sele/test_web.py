def test_web(selenium):
    selenium.get("https://www.baidu.com")
    assert 1==2