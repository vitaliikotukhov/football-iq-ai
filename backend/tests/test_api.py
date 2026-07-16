from fastapi.testclient import TestClient
from app.main import app
client=TestClient(app)
def test_root(): assert client.get("/").status_code==200
def test_version(): assert client.get("/version").json()["version"]=="0.1.3"
def test_builder_catalog():
    r=client.get("/builder/catalog"); assert r.status_code==200; assert any(x["id"]==39 for x in r.json()["competitions"])
