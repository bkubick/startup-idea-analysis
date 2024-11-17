from pydantic import BaseModel


class Market(BaseModel):
    """ Dataclass for a market object. """
    name: str
    description: str
    market_cap: int
    market_share: float
    growth_rate: float
    competitors: list[str]


class Idea(BaseModel):
    """ Dataclass for an idea object. """
    title: str
    description: str
    rating: int | None
    market_name: str
    similar_ideas: list[str]
