from __future__ import annotations

import os
from contextlib import nullcontext
from typing import Any

try:
    from dotenv import load_dotenv
except Exception:  # pragma: no cover
    load_dotenv = None

if load_dotenv is not None:
    load_dotenv()

if os.getenv("LANGFUSE_BASE_URL") and not os.getenv("LANGFUSE_HOST"):
    os.environ["LANGFUSE_HOST"] = os.environ["LANGFUSE_BASE_URL"]

TRACING_BACKEND = "langfuse"
TRACING_IMPORT_ERROR: str | None = None

try:
    from langfuse import get_client, observe

    class _LangfuseV3Context:
        def update_current_trace(self, **kwargs: Any) -> None:
            get_client().update_current_trace(**kwargs)

        def update_current_observation(self, **kwargs: Any) -> None:
            metadata = kwargs.get("metadata") or {}
            usage_details = kwargs.get("usage_details")
            if usage_details:
                metadata = {**metadata, "usage_details": usage_details}
            get_client().update_current_span(metadata=metadata or None)

        def score_current_trace(self, *, name: str, value: float | str, data_type: str = "NUMERIC") -> None:
            get_client().score_current_trace(name=name, value=value, data_type=data_type)

        def start_as_current_span(self, *, name: str, metadata: dict[str, Any] | None = None):
            return get_client().start_as_current_span(name=name, metadata=metadata)

        def flush(self) -> None:
            get_client().flush()

    langfuse_context = _LangfuseV3Context()
except Exception as exc:  # pragma: no cover
    TRACING_BACKEND = "disabled"
    TRACING_IMPORT_ERROR = type(exc).__name__

    def observe(*args: Any, **kwargs: Any):
        def decorator(func):
            return func
        return decorator

    class _DummyContext:
        def update_current_trace(self, **kwargs: Any) -> None:
            return None

        def update_current_observation(self, **kwargs: Any) -> None:
            return None

        def score_current_trace(self, *, name: str, value: float | str, data_type: str = "NUMERIC") -> None:
            return None

        def start_as_current_span(self, *, name: str, metadata: dict[str, Any] | None = None):
            return nullcontext()

        def flush(self) -> None:
            return None

    langfuse_context = _DummyContext()


def tracing_enabled() -> bool:
    return bool(os.getenv("LANGFUSE_PUBLIC_KEY") and os.getenv("LANGFUSE_SECRET_KEY"))


def tracing_backend() -> str:
    return TRACING_BACKEND if tracing_enabled() else "disabled"
