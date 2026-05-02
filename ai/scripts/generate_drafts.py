"""Generates all draft outputs to docs/draft/ for manual review."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DRAFT_DIR = ROOT / "docs" / "draft"
DRAFT_DIR.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(ROOT / "ai" / "agents"))

import update_bio
import update_about
import update_readme_en
import update_readme_pt

print("=" * 60)
print("Atlas AI — generating drafts to docs/draft/")
print("=" * 60)

tasks = [
    (update_bio,       DRAFT_DIR / "bio.txt"),
    (update_about,     DRAFT_DIR / "about.md"),
    (update_readme_en, DRAFT_DIR / "README.en.md"),
    (update_readme_pt, DRAFT_DIR / "README.pt.md"),
]

for module, out_path in tasks:
    print(f"\n{'─'*60}")
    print(f"→ {module.__name__}  →  {out_path.relative_to(ROOT)}")
    print(f"{'─'*60}")
    try:
        module.main(output_file=out_path)
    except Exception as e:
        print(f"[ERROR] {module.__name__}: {e}")

print("\n" + "=" * 60)
print("Drafts saved to docs/draft/. Review before promoting to docs/.")
print("=" * 60)
