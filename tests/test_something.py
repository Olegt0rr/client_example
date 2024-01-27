import pytest
from app.client import WeatherClient


@pytest.fixture(name="weather_client")
async def weather_client_fixture():
    client = WeatherClient()
    yield client
    await client.close()


@pytest.fixture(name="prepare_db")
async def prepare_db_fixture():
    async with session.begin():
        statement = "SELECT 1"
        await session.execute(statement)

    yield

    async with session.begin():
        statement = "SELECT 1"
        await session.execute(statement)


async def test_weather(weather_client, prepare_db):
    data = weather_client_fixture.get_weather()
    assert data == {"temperature": 1}

async def test_weather(weather_client, prepare_db):
    data = weather_client_fixture.get_weather()
    assert data == {"temperature": 1}

async def test_weather(weather_client, prepare_db):
    data = weather_client_fixture.get_weather()
    assert data == {"temperature": 1}

async def test_weather(weather_client, prepare_db):
    data = weather_client_fixture.get_weather()
    assert data == {"temperature": 1}
