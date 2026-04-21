"""Quick smoke test for the Anthropic provider via LLMClient."""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from llm_client import LLMClient

os.environ.setdefault("LLM_PROVIDER", "anthropic")

client = LLMClient()

prompt = (
    "Write a one-sentence professional bio for a backend developer "
    "specializing in Java, Python, and DevOps."
)

start = time.monotonic()
output = client.generate(prompt, task="short_text")
elapsed = time.monotonic() - start

print(f"provider : {client.provider}")
print(f"model    : claude-sonnet-4-5")
print(f"elapsed  : {elapsed:.2f}s")
print(f"output   : {output}")
