from llm_client import LLMClient

client = LLMClient()

response = client.generate(
    prompt="Write a one sentence professional summary for a backend developer specialized in Java, Python, APIs and DevOps."
)

print(response)

