from pydantic import BaseModel, Field


class Market(BaseModel):
    """ Dataclass for a market object. """
    name: str = Field(description="The name of the market.")
    description: str = Field(description="A brief description of the market.")
    market_cap: int = Field(description="The market capitalization of the market.")
    growth_rate: float = Field(description="The growth rate of the market.")
    competitors: list[str] = Field([], description="A list of competitors in the market.")


class Idea(BaseModel):
    """ Dataclass for an idea object. """
    title: str = Field(description="The title of the idea.")
    description: str = Field(description="A brief description of the idea.")
    rating: int | None = Field(None, description="The rating of the idea.")
    existing_ideas: list[str] = Field([], description="A list of existing ideas.")
    market: Market = Field(description="The market of the idea.")
    idea_type: str = Field(description="The type of the idea. (e.g. product, service, website, etc.)")
    industry: str = Field(description="The industry of the idea. (e.g. technology, healthcare, finance, etc.)")
    tags: list[str] = Field([], description="A list of tags for the idea.")
    notes: str | None = Field(None, description="Additional notes for the idea.")
