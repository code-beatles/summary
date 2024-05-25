from __future__ import annotations

from summary import youtube


async def test_get_captions():
    from summary import youtube

    captions = await youtube.get_captions("gqaHkPEZAew")
    assert captions


async def test_download(captions):
    data = await youtube.download_caption(captions[1].url)
    assert data
    text = " ".join([item["text"] for item in data])
    assert text
