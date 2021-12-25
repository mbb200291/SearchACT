from pydantic import BaseModel
from pydantic import Field


class Department(BaseModel):
    id: str = Field(None, title="id of department", description="id of department")
    name: str = Field(..., title="name of department", description="name of department")
    abbreviation: str = Field(
        ...,
        title="abbreviation of department",
        description="abbreviation of department",
    )
    active: bool = Field(
        ..., title="active of department", description="active of department"
    )

    class Config:
        orm_mode = True
