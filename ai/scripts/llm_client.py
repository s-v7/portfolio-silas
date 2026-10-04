from __future__ import annotations

import os
import sys
from typing import Any

import httpx

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "core"))
from model_router import get_model

try:
    import anthropic as _anthropic_sdk
    _ANTHROPIC_AVAILABLE = True
except ImportError:
    _ANTHROPIC_AVAILABLE = False


class LLMClient:
    def __init__(self) -> None:
        self.provider = os.getenv("LLM_PROVIDER", "openai").lower()
        self.api_key = os.getenv("LLM_API_KEY") or os.getenv("OPENAI_API_KEY")
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        self.max_tokens = int(os.getenv("LLM_MAX_TOKENS", "2000"))

        self.last_provider: str = self.provider
        self.last_model: str = ""

        if self.provider == "anthropic" and not self.anthropic_api_key:
            print("[LLMClient] ANTHROPIC_API_KEY não configurada — usando fallback para OpenAI")
            self.provider = "openai"

        if self.provider == "openai" and not self.api_key:
            raise ValueError("LLM_API_KEY / OPENAI_API_KEY não definida no ambiente.")

        if self.provider == "anthropic":
            if not _ANTHROPIC_AVAILABLE:
                raise ImportError("Pacote anthropic não instalado (pip install anthropic).")
            self._anthropic_async_client = _anthropic_sdk.AsyncAnthropic(api_key=self.anthropic_api_key)
            self._anthropic_sync_client = _anthropic_sdk.Anthropic(api_key=self.anthropic_api_key)

    def _build_openai_payload(self, prompt: str, model: str) -> dict[str, Any]:
        """Constrói o payload padronizado para a API do OpenAI."""
        payload: dict[str, Any] = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
        }
        # Modelos de raciocínio (ex: o1, o3-mini) usam max_completion_tokens; outros usam max_tokens.
        if model.startswith(("o1", "o3")):
            payload["max_completion_tokens"] = self.max_tokens
        else:
            payload["max_tokens"] = self.max_tokens

        return payload

    async def generate_async(self, prompt: str, task: str = "short_text") -> str:
        """Executa a geração de texto de forma ASSÍNCRONA."""
        model = get_model(task, self.provider)
        self.last_provider = self.provider
        self.last_model = model

        print(f"[LLMClient-Async] provider={self.last_provider} model={self.last_model}")

        if self.provider == "anthropic":
            try:
                message = await self._anthropic_async_client.messages.create(
                    model=model,
                    max_tokens=self.max_tokens,
                    messages=[{"role": "user", "content": prompt}],
                )
                return message.content[0].text.strip()
            except Exception as e:
                print(f"[LLMClient-Async] Erro Anthropic: {e} — executando fallback para OpenAI")
                if not self.api_key:
                    raise ValueError("API Key do OpenAI não encontrada para fallback.") from e
                self.last_provider = "openai"
                self.last_model = get_model(task, "openai")
                return await self._generate_openai_async(prompt, self.last_model)

        return await self._generate_openai_async(prompt, model)

    async def _generate_openai_async(self, prompt: str, model: str) -> str:
        base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
        endpoint = f"{base_url}/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = self._build_openai_payload(prompt, model)

        async with httpx.AsyncClient(timeout=60.0, http2=False) as client:
            response = await client.post(
                endpoint,
                headers=headers,
                json=payload,
            )

        if response.status_code != 200:
            raise RuntimeError(f"LLM Async Error ({response.status_code}): {response.text}")

        data = response.json()
        return data["choices"][0]["message"].get("content", "").strip()

    def _generate_openai_sync(self, prompt: str, model: str) -> str:
        base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
        endpoint = f"{base_url}/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = self._build_openai_payload(prompt, model)

        with httpx.Client(timeout=60.0, http2=False) as client:
            response = client.post(
                endpoint,
                headers=headers,
                json=payload,
            )

        if response.status_code != 200:
            raise RuntimeError(f"LLM Sync Error ({response.status_code}): {response.text}")

        data = response.json()
        return data["choices"][0]["message"].get("content", "").strip()

    def generate(self, prompt: str, task: str = "short_text") -> str:
        """Executa a geração de texto de forma SÍNCRONA."""
        model = get_model(task, self.provider)
        self.last_provider = self.provider
        self.last_model = model

        print(f"[LLMClient-Sync] provider={self.last_provider} model={self.last_model}")

        if self.provider == "anthropic":
            try:
                message = self._anthropic_sync_client.messages.create(
                    model=model,
                    max_tokens=self.max_tokens,
                    messages=[{"role": "user", "content": prompt}],
                )
                return message.content[0].text.strip()
            except Exception as e:
                print(f"[LLMClient-Sync] Erro Anthropic: {e} — executando fallback para OpenAI")
                if not self.api_key:
                    raise ValueError("API Key do OpenAI não encontrada para fallback.") from e
                self.last_provider = "openai"
                self.last_model = get_model(task, "openai")
                return self._generate_openai_sync(prompt, self.last_model)

        return self._generate_openai_sync(prompt, model)

    def _generate_openai_sync(self, prompt: str, model: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = self._build_openai_payload(prompt, model)

        with httpx.Client(timeout=60.0) as client:
            response = client.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=payload,
            )

        if response.status_code != 200:
            raise RuntimeError(f"LLM Sync Error ({response.status_code}): {response.text}")

        data = response.json()
        return data["choices"][0]["message"].get("content", "").strip()

