import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT / "ai" / "scripts"))
sys.path.append(str(ROOT / "ai" / "core"))

import json
from llm_client import LLMClient
from context_collector import ContextCollector
from model_router import get_model

OUTPUT_FILE = Path("docs/about.md")

def load_prompt(context: dict) -> str:
    prompt_path = Path("ai/prompts/update_about.md")
    base_prompt = prompt_path.read_text(encoding="utf-8")
    return base_prompt.replace("{{CONTEXT}}", json.dumps(context, indent=2))

def main(output_file: Path = OUTPUT_FILE):
    print("Generating About section with Atlas AI...")

    collector = ContextCollector(repo_root=".")
    context = collector.collect()
    context["repo_structure"] = context["repo_structure"][:10]
    context["recent_commits"] = context["recent_commits"][:3]

    client = LLMClient()
    prompt = load_prompt(context)
    about = client.generate(prompt, task="short_text")
    print(f"[update_about] provider={client.provider} model={get_model('short_text', client.provider)}")

    if not about or not about.strip():
        raise RuntimeError("LLM returned empty about section.")

    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(about.strip(), encoding="utf-8")

    print("About section generated successfully!")
    print("REVIEW:")
    print(about)

if __name__ == "__main__":
    main()
