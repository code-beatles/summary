from __future__ import annotations

from base64 import b64encode

from blackboxprotobuf import encode_message
from httpx import AsyncClient
from muffin_apiclient import Plugin as APIClient

typedef = {"1": {"type": "string"}, "2": {"type": "string"}}
client = AsyncClient()


class Youtube(APIClient):
    name = "youtube"
    root_url = "https://www.googleapis.com/youtube/v3"

    def setup(self, app, **options):
        super().setup(app, **options)

        @self.client.middleware
        async def authorize(method, url, options):
            options["params"] = options.get("params", {})
            options["params"]["key"] = app.cfg.GOOGLE_API_KEY
            return method, url, options

    async def get_captions(self, video_id: str) -> dict:
        return await self.api.captions.get(
            params={
                "part": "snippet",
                "videoId": video_id,
            }
        )

    async def get_caption(self, caption_id: str) -> str:
        return await self.api.captions[caption_id].get()


def get_base64_protobuf(message, typedef):
    data = encode_message(message, typedef)
    return b64encode(data).decode("ascii")
