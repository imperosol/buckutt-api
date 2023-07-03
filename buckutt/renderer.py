import orjson
from ninja.renderers import BaseRenderer


class ORJsonRenderer(BaseRenderer):
    media_type = "application/json"

    def render(self, request, data, *, response_status: int):
        return orjson.dumps(data)
