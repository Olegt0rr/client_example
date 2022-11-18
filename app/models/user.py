
class User(BaseDbModel):
    """Represents database model."""

    name: str = Field(String(255))
