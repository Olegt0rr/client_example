from fastapi import Request
from fastapi.testclient import TestClient

from app.main import my_app


@my_app.get("/weather")
async def get_weather(request: Request):
    return {"temperature": 20}


client = TestClient(my_app)


def test_weather():
    response = client.get("/weather")
    assert response.status_code == 200
