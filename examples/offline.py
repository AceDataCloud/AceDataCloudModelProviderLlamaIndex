"""Native LLM consumer using synthetic HTTP, no real key or request."""

import asyncio
import json

import respx
from llama_index.core.llms import ChatMessage

from llama_index.llms.acedatacloud import AceDataCloud


async def main():
    with respx.mock(assert_all_mocked=True) as router:
        router.post("https://api.acedata.cloud/openai/chat/completions").respond(
            200,
            json={
                "id": "synthetic",
                "object": "chat.completion",
                "created": 0,
                "model": "selected-model",
                "choices": [
                    {
                        "index": 0,
                        "message": {"role": "assistant", "content": "Synthetic reply"},
                        "finish_reason": "stop",
                    }
                ],
                "usage": {"prompt_tokens": 1, "completion_tokens": 2, "total_tokens": 3},
            },
        )
        llm = AceDataCloud(model="selected-model", context_window=4096, api_token="offline-dummy")
        reply = await llm.achat([ChatMessage(role="user", content="test")])
        assert reply.message.content == "Synthetic reply" and len(router.calls) == 1
        assert "offline-dummy" not in llm.model_dump_json()
        print(json.dumps({"mode": "synthetic-offline", "class": llm.class_name(), "reply": reply.message.content}))


if __name__ == "__main__":
    asyncio.run(main())
