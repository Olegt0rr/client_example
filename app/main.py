import asyncio
import logging
import sys

import uvicorn
from fastapi import Depends, FastAPI, Request
from sqlalchemy.ext.asyncio import AsyncSession

from . import models, schemas
from .services import WeatherClient

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/weather")
def get_weather(request: Request):
    weather_client: WeatherClient = request.app.state.weather_client
    data = await weather_client.get_current_weather()
    return data


@app.get("/user/{id}", response_model=schemas.User)
def get_user(id: int, db: AsyncSession = Depends(...)):
    """Shows how to split database model and representation schema."""
    user = await db.get(models.User, id)
    return schemas.User(name=user.name)


@app.on_event("startup")
async def on_startup():
    weather_client = WeatherClient()
    app.state.weather_client = weather_client


@app.on_event("shutdown")
async def on_shutdown():
    weather_client: WeatherClient = app.state.weather_client

    await asyncio.gather(
        weather_client.close(),
    )


if __name__ == "__main__":
    uvicorn.run(app)
