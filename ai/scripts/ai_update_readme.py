
import json
import shutil
from datetime import datetime, timezone
from llm_client import LLMClient
from context_collector import ContextCollector


def backup_readme():
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    shutil.copy("README.md", f"README.backup.{ts}.md")

def load_prompt(context_json: dict) -> str:
    with open("ai/prompts/update_readme.md", "r", encoding="utf-8") as svc:
        base_prompt = svc.read()

    return base_prompt.replace("{{CONTEXT}}", json.dumps(context_json, indent=2))

def main():
    collector = ContextCollector(repo_root=".")
    context = collector.collect()

    client = LLMClient()

    context["repo_structure"] = context["repo_structure"][:15]
    context["recent_commits"] = context["recent_commits"][:5]
    prompt = load_prompt(context)
    backup_readme()

    new_readme = client.generate(prompt, task="long_markdown")

    if not new_readme or not new_readme.strip():
        raise RuntimeError("A LLM retornou um conteúdo vazio. README não será sobrescrito.")

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(new_readme)

    print("README.md atualizado com sucesso!")


if __name__ == "__main__":
    main()


