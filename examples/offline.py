"""Native LLM consumer with an in-memory transport, no real key or network."""

import asyncio
import json

import httpx
from llama_index.core.llms import ChatMessage

from llama_index.llms.acedatacloud import AceDataCloud


async def main():
    requests = []

    def respond(request):
        assert request.method == "POST"
        assert str(request.url) == "https://api.acedata.cloud/openai/chat/completions"
        assert json.loads(request.content)["model"] == "selected-model"
        requests.append(request)
        return httpx.Response(
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

    async with httpx.AsyncClient(transport=httpx.MockTransport(respond), trust_env=False) as client:
        llm = AceDataCloud(
            model="selected-model", context_window=4096, api_token="offline-dummy", async_http_client=client
        )
        reply = await llm.achat([ChatMessage(role="user", content="test")])
        assert reply.message.content == "Synthetic reply" and len(requests) == 1
        assert "offline-dummy" not in llm.model_dump_json()
        print(json.dumps({"mode": "synthetic-offline", "class": llm.class_name(), "reply": reply.message.content}))


if __name__ == "__main__":
    asyncio.run(main())
