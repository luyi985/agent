from pydantic import BaseModel, Field

class TravelRequest(BaseModel):
    city: str|None = Field(default=None, description="Name of the city to travel to, if provided, otherwise null")
    days: int|None = Field(default=None,  description="Length of the trip in days, if provided, otherwise null",)
    children: int|None = Field(default=None, ge=0, description="Number of children traveling together, if provided, otherwise null")
    interests: list[str] = Field(description="Travel interests, only include those explicitly mentioned by the user")