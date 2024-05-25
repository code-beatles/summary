from __future__ import annotations

from httpx import AsyncClient
from muffin_apiclient import Plugin as APIClient
from youtube_transcript_api._errors import CouldNotRetrieveTranscript
from youtube_transcript_api._transcripts import (
    TranscriptList,
    TranscriptListFetcher,
    _TranscriptParser,
)

typedef = {"1": {"type": "string"}, "2": {"type": "string"}}
client = AsyncClient()
fetcher = TranscriptListFetcher(client)


class Youtube(APIClient):
    name = "youtube"
    root_url = "https://www.youtube.com"

    async def get_captions(self, video_id: str):
        html = await self.api.watch(params={"v": video_id})
        try:
            tl = TranscriptList.build(
                client, video_id, fetcher._extract_captions_json(html, video_id)
            )
        except CouldNotRetrieveTranscript:
            return []

        tss = [
            *tl._generated_transcripts.values(),
            *tl._manually_created_transcripts.values(),
        ]
        return [
            {
                "language": ts.language_code,
                "auto_generated": ts.is_generated,
                "url": ts._url,
            }
            for ts in tss
        ]

    async def download_caption(self, url: str):
        xml = await self.client.request("GET", url)
        return _TranscriptParser().parse(xml)

    # async def get_captions(self, video_id: str) -> dict:
    #     return await self.api.captions.get(
    #         params={
    #             "part": "snippet",
    #             "videoId": video_id,
    #         }
    #     )

    # async def get_caption(self, caption_id: str) -> str:
    #     return await self.api.captions[caption_id].get()


# ruff: noqa: ERA001
