import os
import requests
from typing import Optional

# Map de modelo por tipo de tarefa
MODEL_BY_TASK = {
        "long_markdown": "gpt-4o-mini",
        "short_text": "gpt-5-mini",
        "analysis": "gpt-5-mini",
}

class LLMClient:
    def __init__(self):
        self.provider = os.getenv("LLM_PROVIDER", "openai")
        self.api_key = os.getenv("LLM_API_KEY")

        self.default_model = os.getenv("LLM_DEFAULT_MODEL", "gpt-4o-mini")
        self.max_tokens = int(os.getenv("LLM_MAX_TOKENS", "2000"))

        if not self.api_key:
            raise ValueError("LLM_API_KEY não definida no ambiente.")

        if self.provider != "openai":
            raise NotImplementedError(f"Provider {self.provider} ainda não suportado.")

    def generate(self, prompt: str, task: str = "short_text") -> str:
        model = MODEL_BY_TASK.get(task, self.default_model)

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_completion_tokens": self.max_tokens
        }
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=60
        )
        if response.status_code != 200:
            try:
                err = response.json()
                message = err.get("error", {}).get("message", response.text)
            except Exception:
                message = response.text
            raise RuntimeError(
                f"Erro ao chamar LLM: {response.status_code} - {message}"
            )
        data = response.json()
        return data["choices"][0]["message"].get("content", "").strip()
