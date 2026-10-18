# Ace Data Cloud LLM for LlamaIndex

[简体中文](readme/README_zh_Hans.md) · [Models and current pricing](https://platform.acedata.cloud/models?utm_source=llamaindex&utm_medium=referral&utm_campaign=evergreen&utm_content=ace_llm_llamaindex_pricing)

A native `AceDataCloud` LlamaIndex class maintained by Ace Data Cloud. Import it,
choose your model and context size, and use it as `Settings.llm` or an agent's LLM.
The Ace endpoint is preset: you do not manually configure an OpenAI base URL.
This is an independently maintained integration, not default LlamaIndex inclusion.

## 1. Install the integration

Standard package: `llama-index-llms-acedatacloud`; namespace `llama_index.llms.acedatacloud`.
**Source PR stage: not published to PyPI or listed in the official LLM directory yet.**
For source review (Python 3.10+):

```bash
pip install "llama-index-llms-acedatacloud @ git+https://github.com/AceDataCloud/AceDataCloudModelProviderLlamaIndex.git@codex/native-ace-llm"
```

It reuses the official `llama-index-llms-openai-like` implementation for chat,
completion, streaming and tool-call protocols, following the existing OpenRouter
integration pattern. No shared Ace SDK/MCP code is changed. No fallback model is added.

## 2. Register and copy an application API Token

1. [Register or sign in](https://platform.acedata.cloud?utm_source=llamaindex&utm_medium=referral&utm_campaign=evergreen&utm_content=ace_llm_llamaindex_register) and open [Applications](https://platform.acedata.cloud/console/applications?utm_source=llamaindex&utm_medium=referral&utm_campaign=evergreen&utm_content=ace_llm_llamaindex_api_key).
2. Find **General application**; if absent, click **Initialize General Application**.
   General keys have only your account's permitted services; dedicated keys have
   only their application's service. Check selected model access and [price/balance](https://platform.acedata.cloud/models?utm_source=llamaindex&utm_medium=referral&utm_campaign=evergreen&utm_content=ace_llm_llamaindex_balance).
3. Copy the API Key or choose **Manage Keys → Create** for a separate `LlamaIndex LLM` key.

![Real Ace console: copy the redacted application key or manage keys](https://raw.githubusercontent.com/AceDataCloud/SunoDify/8d3d03570e73324220f111f7fe343da0792a8071/_assets/tutorial/get-api-key-en.png)

4. Review **Expiration Time**, **Set Usage Limitation**, **Allowed APIs**. Allow
   `/openai/chat/completions` if restricting APIs; create and copy the key.

![Real Ace console: create a dedicated key with optional restrictions](https://raw.githubusercontent.com/AceDataCloud/SunoDify/8d3d03570e73324220f111f7fe343da0792a8071/_assets/tutorial/create-api-key-en.png)

Screenshots are real redacted Ace console images from the linked SunoDify commit,
retrieved 2026-10-18. The old example name `Dify tutorial` is historical; enter
`LlamaIndex LLM`. These are account setup screenshots, not LlamaIndex model calls.

Copy only the raw token, without `Bearer `, spaces or quotes. Do not use a
`platform-...` management token. Keep it out of prompts, logs, screenshots and Git.

## 3. Select Ace in code

Set `ACEDATACLOUD_API_TOKEN` in your environment or pass `api_token` from a secret
store. `OPENAI_API_KEY` does not replace the Ace token. Constructor and metadata
inspection send no request. Model and context limit must come from your current
available model; there is no hidden model default or fallback.

```python
from llama_index.core import Settings
from llama_index.llms.acedatacloud import AceDataCloud

llm = AceDataCloud(
    model="YOUR_AVAILABLE_CHAT_MODEL",
    context_window=YOUR_MODEL_CONTEXT_TOKEN_LIMIT,
    max_tokens=256,
)
Settings.llm = llm
```

There is no new provider dropdown or GUI promise: LlamaIndex Framework selects
native LLM classes in application code. This gets an Ace class with preset identity,
not merely a tutorial to paste a custom base URL.

## 4. First chat and streaming

The following requests may consume credits; run only with your own approved budget
and a valid model. The placeholders above must be replaced first.

```python
from llama_index.core.llms import ChatMessage

response = llm.chat([ChatMessage(role="user", content="Reply with one short greeting.")])
print(response.message.content)

# A separate billable request if run:
# for chunk in llm.stream_chat([ChatMessage(role="user", content="Say hello.")]):
#     print(chunk.delta or "", end="")
```

Async equivalents are `achat`, `acomplete`, `astream_chat`, `astream_complete`.
Chat is synchronous or streamed text; it does not create a media task to poll.
Suno/Seedance task lookup belongs to the relevant tool integration, not this LLM.

Tool calling is **off by default**. Only pass `is_function_calling_model=True`
for a model whose current contract supports it; then use
`FunctionAgent(llm=llm, tools=your_tools)`. This flag is a caller-selected capability,
not a claim every model supports tools. Structured outputs are not universally enabled.

401/403/429/500 preserve OpenAI-client error categories; retries are fixed to zero.
On ambiguous network errors inspect usage before manually sending another request.
The token is excluded from model repr/serialization. Neither fixed endpoint nor
credentials may be silently overridden through OpenAI keyword arguments.

## 5. Verify free, offline

```bash
pip install -e ".[dev]"
python examples/offline.py
pytest
ruff check .
ruff format --check .
python -m build
```

The consumer uses mocked HTTP and a dummy token, and clearly labels output
`synthetic-offline`. CI builds the wheel and installs it outside the source tree.
No paid chat or production model quality, billing, official listing or revenue is claimed.

| Problem | Check |
|---|---|
| Package absent on PyPI | Initial publication is pending; use the review branch. |
| Missing token / 401 | Use the full raw Ace application token and check expiration/access. |
| 403 / insufficient balance | Check model entitlement and budget, not retries. |
| 429 / ambiguous network error | Automatic retries are off; inspect usage before sending again. |
| Tool call rejected | Only enable tools for models that support the protocol. |
| Wrong context limit | Read the selected model's current limit; this class does not guess. |

## Release and official discovery

The prepared PyPI Trusted Publishing workflow needs project/publisher setup by an
authorized existing PyPI owner: repository `AceDataCloudModelProviderLlamaIndex`,
workflow `publish.yml`, environment `pypi`. Source review and explicit merge/release
approval remain gates. See [distribution handoff](docs/distribution.md).
Official docs/default inclusion and real paid call/billing must be verified separately.

MIT. Maintained by Ace Data Cloud.
