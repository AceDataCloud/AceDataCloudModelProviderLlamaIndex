"""Keep protocol mocks on their explicit HTTPX transport and reject networking."""

import socket

import httpx
import pytest

from llama_index.llms.acedatacloud import AceDataCloud


@pytest.fixture(autouse=True)
async def offline_clients(monkeypatch):
    def deny_network(*args, **kwargs):
        raise AssertionError("Tests must not open a network connection")

    monkeypatch.setattr(socket, "getaddrinfo", deny_network)
    monkeypatch.setattr(socket.socket, "connect", deny_network)
    original_init = AceDataCloud.__init__
    with httpx.Client(trust_env=False) as sync_client:
        async with httpx.AsyncClient(trust_env=False) as async_client:

            def init(self, *args, **kwargs):
                kwargs.setdefault("http_client", sync_client)
                kwargs.setdefault("async_http_client", async_client)
                original_init(self, *args, **kwargs)

            monkeypatch.setattr(AceDataCloud, "__init__", init)
            yield
