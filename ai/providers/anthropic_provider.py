from __future__ import annotations

import os
from typing import Literal, cast

from anthropic import Anthropic
from anthropic.types import MessageParam, TextBlock

from ai.core.contracts import (
    LLMProvider,
    ProviderRequest,
    ProviderResponse,
)
from ai.core.exceptions import ConfigurationError, ProviderError
from ai.core.model_router import get_model

AnthropicRole = Literal["user", "assistant"]


class AnthropicProvider(LLMProvider):
    def __init__(
        self,
        api_key: str | None = None,
    ) -> None:
        resolved_key = api_key or os.getenv("ANTHROPIC_API_KEY")

        if not resolved_key:
            raise ConfigurationError(
                "ANTHROPIC_API_KEY is required."
            )

        self._client = Anthropic(api_key=resolved_key)

    @property
    def name(self) -> str:
        return "anthropic"

    def generate(self, request: ProviderRequest) -> ProviderResponse:
        model = request.model or get_model(
            request.task.value,
            self.name,
        )

        system_messages: list[str] = []
        conversation: list[MessageParam] = []

        for message in request.messages:
            if message.role == "system":
                system_messages.append(message.content)
                continue

            if message.role not in {"user", "assistant"}:
                raise ProviderError(
                    "Anthropic supports only system, user and "
                    "assistant message roles."
                )

            role = cast(AnthropicRole, message.role)

            conversation.append(
                {
                    "role": role,
                    "content": message.content,
                }
            )

        if not conversation:
            raise ProviderError(
                "Anthropic requires at least one user or assistant message."
            )

        try:
            response = self._client.messages.create(
                model=model,
                max_tokens=request.options.max_tokens,
                system="\n\n".join(system_messages),
                messages=conversation,
            )
        except Exception as exc:
            raise ProviderError(
                f"Anthropic request failed: {exc}"
            ) from exc

        text_parts = [
            block.text
            for block in response.content
            if isinstance(block, TextBlock)
        ]

        content = "".join(text_parts).strip()

        if not content:
            raise ProviderError(
                "Anthropic returned an empty textual response."
            )

        return ProviderResponse(
            content=content,
            provider=self.name,
            model=model,
            metadata={
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens,
            },
        )
