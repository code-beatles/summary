from __future__ import annotations

import pytest

pytestmark = pytest.mark.skip(reason="requires API keys")


async def test_base():
    from summary import openai

    res = await openai.api.models()
    assert res

    res = await openai.api.chat.completions.post(
        raise_for_status=False,
        json={
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "system", "content": "You are a chatbot."}],
        },
    )
