from __future__ import annotations


async def test_captions():
    from summary import youtube

    await youtube.get_captions("NOAgplgTxfc")
