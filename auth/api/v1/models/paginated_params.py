from pydantic import BaseModel, Field

PAGE_SIZE = 10


class PaginatedParams(BaseModel):
    page: int = Field(
        default=1,
        gt=0,
        alias="page",
        description="Page number"
    )
    size: int = Field(
        default=PAGE_SIZE,
        gt=0, alias="per_page",
        description="Number of items per page"
    )
