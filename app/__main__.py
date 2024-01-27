import logging
import sys
from contextlib import asynccontextmanager

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


@asynccontextmanager
async def lifespan(application: FastAPI):
    weather_client = WeatherClient()
    application.state["weather_client"] = weather_client
    yield
    await weather_client.close()


app = FastAPI(lifespan=lifespan)


@app.get("/weather")
async def get_weather(request: Request):
    weather_client: WeatherClient = request.app.state.weather_client
    data = await weather_client.get_current_weather()
    return data


@app.get("/user/{id}", response_model=schemas.User)
async def get_user(id: int, db: AsyncSession = Depends()):
    """Shows how to split database model and representation schema."""
    user = await db.get(models.User, id)
    return schemas.User(name=user.name)


if __name__ == "__main__":
    uvicorn.run(app)
