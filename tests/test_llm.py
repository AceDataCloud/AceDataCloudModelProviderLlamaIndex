import json

import pytest
import respx
from llama_index.core import Settings
from llama_index.core.llms import ChatMessage, MockLLM
from openai import AuthenticationError, InternalServerError, PermissionDeniedError, RateLimitError

from llama_index.llms.acedatacloud import AceDataCloud

URL = "https://api.acedata.cloud/openai/chat/completions"


def reply():
    return {
        "id": "synthetic",
        "object": "chat.completion",
        "created": 0,
        "model": "model",
        "choices": [{"index": 0, "message": {"role": "assistant", "content": "hello"}, "finish_reason": "stop"}],
        "usage": {"prompt_tokens": 1, "completion_tokens": 1, "total_tokens": 2},
    }


def test_native_settings_and_secret_exclusion(monkeypatch):
    monkeypatch.setenv("ACEDATACLOUD_API_TOKEN", "test-secret")
    llm = AceDataCloud(model="selected-model", context_window=8000)
    assert llm.class_name() == "AceDataCloud_LLM"
    assert llm.metadata.model_name == "selected-model" and llm.metadata.context_window == 8000
    assert llm.metadata.is_chat_model and not llm.metadata.is_function_calling_model
    assert "test-secret" not in repr(llm) and "test-secret" not in llm.model_dump_json()
    Settings.llm = MockLLM()
    previous = Settings.llm
    try:
        Settings.llm = llm
        assert Settings.llm is llm
    finally:
        Settings.llm = previous


@pytest.mark.parametrize("async_", [False, True])
async def test_chat_and_completion_use_ace_endpoint(async_):
    with respx.mock(assert_all_mocked=True) as router:
        route = router.post(URL).respond(200, json=reply())
        llm = AceDataCloud(model="selected-model", context_window=4096, api_token="token", max_tokens=20)
        messages = [ChatMessage(role="user", content="test")]
        result = await llm.achat(messages) if async_ else llm.chat(messages)
        assert result.message.content == "hello"
        complete = await llm.acomplete("test") if async_ else llm.complete("test")
        assert complete.text == "hello"
        assert route.call_count == 2
        body = json.loads(route.calls[0].request.content)
        assert body["model"] == "selected-model" and body["max_tokens"] == 20
        assert route.calls[0].request.headers["Authorization"] == "Bearer token"


@pytest.mark.parametrize("async_", [False, True])
async def test_streaming_protocol(async_):
    chunks = [
        {
            "id": "s",
            "object": "chat.completion.chunk",
            "created": 0,
            "model": "model",
            "choices": [{"index": 0, "delta": {"role": "assistant", "content": "hello"}, "finish_reason": None}],
        },
        {
            "id": "s",
            "object": "chat.completion.chunk",
            "created": 0,
            "model": "model",
            "choices": [{"index": 0, "delta": {}, "finish_reason": "stop"}],
        },
    ]
    data = "".join("data: " + json.dumps(c) + "\n\n" for c in chunks) + "data: [DONE]\n\n"
    with respx.mock(assert_all_mocked=True) as router:
        router.post(URL).respond(200, text=data, headers={"content-type": "text/event-stream"})
        llm = AceDataCloud(model="model", context_window=4096, api_token="token")
        if async_:
            stream = await llm.astream_chat([ChatMessage(role="user", content="test")])
            results = [r async for r in stream]
        else:
            results = list(llm.stream_chat([ChatMessage(role="user", content="test")]))
        assert "".join(r.delta or "" for r in results) == "hello"


@pytest.mark.parametrize(
    "status,error",
    [(401, AuthenticationError), (403, PermissionDeniedError), (429, RateLimitError), (500, InternalServerError)],
)
@pytest.mark.parametrize("async_", [False, True])
async def test_errors_no_retry(status, error, async_):
    with respx.mock(assert_all_mocked=True) as router:
        route = router.post(URL).respond(status, json={"error": {"message": "rejected", "type": "error"}})
        llm = AceDataCloud(model="model", context_window=4096, api_token="token")
        with pytest.raises(error):
            if async_:
                await llm.achat([ChatMessage(role="user", content="test")])
            else:
                llm.chat([ChatMessage(role="user", content="test")])
        assert route.call_count == 1


@pytest.mark.parametrize("token", ["", " ", "Bearer key", "platform-management"])
def test_invalid_token(token):
    with pytest.raises(ValueError):
        AceDataCloud(model="model", context_window=4096, api_token=token)


@pytest.mark.parametrize(
    "kwargs",
    [
        {"api_base": "https://other.invalid"},
        {"api_key": "other"},
        {"max_retries": 3},
        {"is_chat_model": False},
        {"api_version": "other"},
    ],
)
def test_cannot_override_provider_identity(kwargs):
    with pytest.raises(ValueError):
        AceDataCloud(model="model", context_window=4096, api_token="token", **kwargs)


@pytest.mark.parametrize("model,context", [("", 4096), ("model", 0), ("model", True)])
def test_explicit_model_and_context(model, context):
    with pytest.raises(ValueError):
        AceDataCloud(model=model, context_window=context, api_token="token")


def test_tool_capability_is_opt_in():
    llm = AceDataCloud(model="supported-model", context_window=4096, api_token="token", is_function_calling_model=True)
    assert llm.metadata.is_function_calling_model


async def test_function_call_protocol_is_model_opt_in():
    from llama_index.core.tools import FunctionTool

    def music_status(task_id: str) -> str:
        """Read music task status."""
        return task_id

    with respx.mock(assert_all_mocked=True) as router:
        response = reply()
        response["choices"][0]["message"] = {
            "role": "assistant",
            "content": None,
            "tool_calls": [
                {
                    "id": "call-1",
                    "type": "function",
                    "function": {"name": "music_status", "arguments": '{"task_id":"old-task"}'},
                }
            ],
        }
        response["choices"][0]["finish_reason"] = "tool_calls"
        route = router.post(URL).respond(200, json=response)
        llm = AceDataCloud(
            model="tool-capable-model", context_window=4096, api_token="token", is_function_calling_model=True
        )
        result = await llm.achat_with_tools([FunctionTool.from_defaults(music_status)], user_msg="check status")
        calls = llm.get_tool_calls_from_response(result)
        assert calls[0].tool_name == "music_status" and calls[0].tool_kwargs == {"task_id": "old-task"}
        assert json.loads(route.calls[0].request.content)["tools"][0]["function"]["name"] == "music_status"
