from __future__ import annotations

from . import Summary, Video


async def test_video():
    assert await Video.create(id="NOAgplgTxfc")


async def test_summary(caption):
    summary = await Summary.generate(caption)
    assert summary
