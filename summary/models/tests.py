from __future__ import annotations

from . import Video


async def test_video():
    assert await Video.create(id="NOAgplgTxfc")
