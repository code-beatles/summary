from __future__ import annotations


async def test_index(client):
    res = await client.get("/")
    assert res.status_code == 200
