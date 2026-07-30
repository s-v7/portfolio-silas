from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "dist_worker_context.js"

SOURCES = [
    ("Knowledge CV", ROOT / "ai/knowledge/cv.md"),
    ("Knowledge Experience", ROOT / "ai/knowledge/experience.md"),
    ("Knowledge Skills", ROOT / "ai/knowledge/skills.md"),
    ("Knowledge Education", ROOT / "ai/knowledge/education.md"),
    ("Frontend Data CV", ROOT / "src/data/cv.ts"),
    ("Frontend Data Experience", ROOT / "src/data/experience.ts"),
    ("Frontend Data Education", ROOT / "src/data/education.ts"),
    ("Frontend Data Projects", ROOT / "src/data/projects.ts"),
    ("Frontend Data Knowledge Base", ROOT / "src/data/knowledgeBase.ts"),
    ("Frontend Data AI Tools", ROOT / "src/data/aiTools.ts"),
    ("Frontend Data Prompt Cards", ROOT / "src/data/promptCards.ts"),
    ("Frontend Data Skill Cards", ROOT / "src/data/skillCards.ts"),
    ("Frontend Data What I Do", ROOT / "src/data/whatIDo.ts"),
]

def clean_ts(text: str) -> str:
    text = re.sub(r"import .*?;\n", "", text)
    text = re.sub(r"export type .*?};", "", text, flags=re.S)
    text = text.replace("export const", "const")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()

parts = []
for title, path in SOURCES:
    if not path.exists():
        continue

    raw = path.read_text(encoding="utf-8").strip()
    content = clean_ts(raw) if path.suffix in {".ts", ".tsx"} else raw
    parts.append(f"# {title}\n\n{content}")

context = "\n\n---\n\n".join(parts)

OUT.write_text(
    "export const PROFILE_CONTEXT = "
    + json.dumps(context, ensure_ascii=False, indent=2)
    + ";\n",
    encoding="utf-8",
)

print(f"Generated {OUT} ({len(context)} chars)")
