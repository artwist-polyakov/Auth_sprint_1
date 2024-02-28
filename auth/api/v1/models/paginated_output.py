from api.v1.models.output import Output


class PaginatedOutput(Output):
    total: int
    page: int
    pages: int
    per_page: int
    results: list[dict]
