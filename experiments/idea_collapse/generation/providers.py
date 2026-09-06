"""Small injectable provider boundary. No provider is called automatically."""

from dataclasses import dataclass
import json
from typing import Protocol

from .schema import IDEA_FIELDS


@dataclass(frozen=True)
class Response:
    text: str
    raw: str
    resolved_model: str | None
    version_evidence: str
    refusal: bool = False


class ProviderFailure(Exception):
    def __init__(self, code, raw=""):
        super().__init__(code)
        self.code = code
        self.raw = raw


class Provider(Protocol):
    def generate(self, request: dict) -> Response: ...


class MockProvider:
    """Explicit fixtures, never a stand-in for scientific evidence."""
    def __init__(self, mode="success"):
        self.mode = mode
        self.calls = 0

    def generate(self, request):
        if request["run_purpose"] != "mock":
            raise ValueError("mock provider only accepts mock purpose")
        self.calls += 1
        version = request["model_version"]
        if self.mode == "provider_error":
            raise ProviderFailure("mock_provider_error", "MOCK: simulated transport failure")
        if self.mode == "refusal":
            return Response("MOCK refusal", "MOCK refusal", version, "mock_fixture", True)
        if self.mode == "malformed":
            return Response("MOCK not JSON", "MOCK not JSON", version, "mock_fixture")
        text = json.dumps({key: f"MOCK ONLY {key}: seed {request['seed']}" for key in IDEA_FIELDS})
        return Response(text, text, version, "mock_fixture")


class OpenAICompatibleProvider:
    """An injected transport can support multiple explicitly configured families.

    Transport/credentials/consent are deployment responsibilities. This adapter
    has no default network implementation and cannot spend money on import.
    """
    def __init__(self, transport):
        self.transport = transport

    def generate(self, request):
        settings = request["generation_settings"]
        if set(settings) - {"temperature", "top_p", "max_tokens"}:
            raise ValueError("settings cannot override identity, messages or seed")
        payload = {"model": request["model_version"], "seed": request["seed"],
                   "messages": [{"role": "system", "content": request["prompt"]}],
                   **settings}
        raw = self.transport(payload)
        try:
            data = json.loads(raw)
            message = data["choices"][0]["message"]
            content = message.get("content")
            refusal = message.get("refusal")
            if content is None and not refusal:
                raise ValueError("missing text")
            if content is not None and not isinstance(content, str):
                raise ValueError("non-text content")
            return Response(content or "", raw, data.get("model"),
                            "provider_reported_not_independently_verified", bool(refusal))
        except (ValueError, TypeError, KeyError, IndexError):
            raise ProviderFailure("malformed_provider_envelope", raw) from None
