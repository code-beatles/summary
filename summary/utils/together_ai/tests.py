from __future__ import annotations

from summary import together_ai


async def test_base():
    res = await together_ai.api.models()
    assert res

    res = await together_ai.api.chat.completions.post(
        raise_for_status=False,
        json={
            "model": "meta-llama/Llama-3-8b-chat-hf",
            "messages": [{"role": "system", "content": "You are a chatbot."}],
        },
    )
    assert res


async def test_summarize(caption):
    assert caption.data
    assert caption.text
    text_8kb = caption.text[:8000]
    promt = f"Summarize the following in 5 bullet points: {text_8kb}"

    res = await together_ai.api.chat.completions.post(
        raise_for_status=False,
        json={
            "model": "meta-llama/Llama-3-8b-chat-hf",
            "messages": [{"role": "system", "content": promt}],
        },
    )
    assert res
