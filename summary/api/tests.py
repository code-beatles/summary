from __future__ import annotations

from summary.models import Video


async def test_youtube(client):
    video_id = "NOAgplgTxfc"
    res = await client.get(f"/api/v1/youtube/{video_id}")
    assert res.status_code == 200

    video = await Video.get(id=video_id)
    assert video
    assert video.summary_updated is None
    assert video.captions_updated is None


async def test_youtube_captions(client):
    video_id = "gqaHkPEZAew"
    res = await client.get(f"/api/v1/youtube/{video_id}/captions")
    assert res.status_code == 200
    data = await res.json()
    assert data

    video = await Video.get(id=video_id)
    assert video
    assert await video.captions


async def test_youtube_caption(client, captions):
    video_id = "gqaHkPEZAew"
    res = await client.get(f"/api/v1/youtube/{video_id}/captions/{captions[0].id}")
    assert res.status_code == 200
    data = await res.json()
    assert data
    assert data["data"]

    video = await Video.get(id=video_id)
    assert video
    assert await video.captions
