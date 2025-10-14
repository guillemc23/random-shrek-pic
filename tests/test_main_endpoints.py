from fastapi.testclient import TestClient


def test_info_endpoint():
    import main

    client = TestClient(main.app)
    r = client.get("/info")
    assert r.status_code == 200
    body = r.json()
    # ensure the endpoint returns the app version
    assert body.get("version") == main.app.version


def test_redirect_endpoints(monkeypatch):
    import main

    client = TestClient(main.app)

    stub = "http://example.test/fake.jpg"

    # Replace random_line with a deterministic stub so we don't depend on the data files or randomness
    monkeypatch.setattr(main, "random_line", lambda path: stub)

    # Test root and alias
    for path in ["/", "/shrek", "/toilet", "/swamp", "/cursed"]:
        # TestClient follows redirects by default, so perform the GET and check the final URL
        resp = client.get(path)
        # final response should be successful (200) if the stub URL is reachable by TestClient
        # or it may be a redirect if TestClient doesn't actually perform external redirects; in
        # either case ensure the Location header on the initial response (if present) matches stub
        if resp.status_code in (301, 302, 307, 308):
            assert resp.headers.get("location") == stub
        else:
            # When TestClient follows the redirect, the final URL is available via resp.url
            assert str(resp.url).startswith(stub)
