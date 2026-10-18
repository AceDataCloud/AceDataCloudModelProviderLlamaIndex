"""Ace Data Cloud LLM using official OpenAILike protocols."""

from __future__ import annotations

import os
from typing import Any

from llama_index.core.bridge.pydantic import Field
from llama_index.llms.openai_like import OpenAILike

API_BASE = "https://api.acedata.cloud/openai"


class AceDataCloud(OpenAILike):
    """Ace native LLM; explicit model/context, application token, no fallback.

    Chat/completion/streaming and tool protocols reuse official OpenAILike.
    Tool calling is opt-in per model. Construction sends no request.
    """

    api_key: str | None = Field(default=None, exclude=True, repr=False)

    def __init__(
        self,
        model: str,
        context_window: int,
        api_token: str | None = None,
        is_function_calling_model: bool = False,
        **kwargs: Any,
    ) -> None:
        token = api_token if api_token is not None else os.environ.get("ACEDATACLOUD_API_TOKEN", "")
        if not token or not token.strip():
            raise ValueError("Set ACEDATACLOUD_API_TOKEN to your raw application token")
        token = token.strip()
        if token.lower().startswith("bearer ") or token.startswith("platform-"):
            raise ValueError("Use a raw application API token, without Bearer; not an account-management token")
        if not model or not model.strip():
            raise ValueError("Choose an available model explicitly")
        if isinstance(context_window, bool) or context_window <= 0:
            raise ValueError("context_window must be a positive token limit for your selected model")
        fixed = {"api_key", "api_base", "api_version", "is_chat_model", "max_retries"} & kwargs.keys()
        if fixed:
            raise ValueError("Ace identity and retries are fixed: " + ", ".join(sorted(fixed)))
        super().__init__(
            model=model.strip(),
            context_window=context_window,
            api_key=token,
            api_base=API_BASE,
            is_chat_model=True,
            is_function_calling_model=is_function_calling_model,
            max_retries=0,
            **kwargs,
        )

    @classmethod
    def class_name(cls) -> str:
        return "AceDataCloud_LLM"
