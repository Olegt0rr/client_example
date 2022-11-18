from pydantic import BaseModel, Field


class User(BaseModel):
    """Represents json schema."""

    name: str = Field(description="Example of description")
