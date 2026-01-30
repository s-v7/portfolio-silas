import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT / "ai" / "scripts"))

import json
from llm_client import LLMClient
from context_collector import ContextCollector



OUTPUT_FILE = Path("docs/bio.txt")

def load_prompt(context: dict) -> str:
    prompt_path = Path("ai/prompts/update_bio.md")
    base_prompt = prompt_path.read_text(encoding="utf-8")
    return base_prompt.replace("{{CONTEXT}}", json.dumps(context, indent=2))

def main():
    print("Generating professional bio with Atlas AI...")

    collector = ContextCollector(repo_root=".")
    context = collector.collect()

    context["repo_structure"] = context["repo_structure"][:10]
    context["recent_commits"] = context["recent_commits"][:3]

    client = LLMClient()

    prompt = load_prompt(context)
    bio = client.generate(prompt, task="short_text")

    if not bio or not bio.strip():
        raise RuntimeError("LLM returned empty bio.")

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(bio.strip(), encoding="utf-8")

    print("Bio generated successfully!")
    print("REVIEW:")
    print(bio)

if __name__ == '__main__':
    main()


