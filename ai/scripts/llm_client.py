import os
import sys
import requests
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "core"))
from model_router import get_model

try:
    import anthropic as _anthropic_sdk
    _ANTHROPIC_AVAILABLE = True
except ImportError:
    _ANTHROPIC_AVAILABLE = False


class LLMClient:
    def __init__(self):
        self.provider = os.getenv("LLM_PROVIDER", "openai")
        self.api_key = os.getenv("LLM_API_KEY")
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        self.max_tokens = int(os.getenv("LLM_MAX_TOKENS", "2000"))

        # ── expose after each generate() call ──
        self.last_provider: str = self.provider
        self.last_model: str = ""

        if self.provider == "anthropic" and not self.anthropic_api_key:
            print("[LLMClient] ANTHROPIC_API_KEY not set — falling back to OpenAI")
            self.provider = "openai"

        if self.provider == "openai":
            if not self.api_key:
                raise ValueError("LLM_API_KEY not set in environment.")

        if self.provider == "anthropic":
            if not _ANTHROPIC_AVAILABLE:
                raise ImportError("anthropic package not installed (pip install anthropic).")
            self._client = _anthropic_sdk.Anthropic(api_key=self.anthropic_api_key)

    def generate(self, prompt: str, task: str = "short_text") -> str:
        model = get_model(task, self.provider)

        # record what was actually used
        self.last_provider = self.provider
        self.last_model = model

        print(f"[LLMClient] provider={self.last_provider} model={self.last_model}")

        if self.provider == "anthropic":
            try:
                return self._generate_anthropic(prompt, model)
            except Exception as e:
                print(f"[LLMClient] Anthropic error: {e} — falling back to OpenAI")
                if not self.api_key:
                    raise
                self.last_provider = "openai"
                self.last_model = get_model(task, "openai")
                print(f"[LLMClient] fallback provider={self.last_provider} model={self.last_model}")
                return self._generate_openai(prompt, self.last_model)

        return self._generate_openai(prompt, model)

    def _generate_anthropic(self, prompt: str, model: str) -> str:
        message = self._client.messages.create(
            model=model,
            max_tokens=self.max_tokens,
            messages=[{"role": "user", "content": prompt}],
        )
        return message.content[0].text.strip()

    def _generate_openai(self, prompt: str, model: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_completion_tokens": self.max_tokens,
        }
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=60,
        )
        if response.status_code != 200:
            try:
                err = response.json()
                message = err.get("error", {}).get("message", response.text)
            except Exception:
                message = response.text
            raise RuntimeError(f"LLM error: {response.status_code} - {message}")
        data = response.json()
        return data["choices"][0]["message"].get("content", "").strip()
