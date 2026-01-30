import os
import subprocess
import json
from datetime import datetime, timezone

class ContextCollector:
    def __init__(self, repo_root="."):
        self.repo_root = os.path.abspath(repo_root)

    def get_repo_structure(self):
        structure = []
        for root, dirs, files in os.walk(self.repo_root):
            # ignora node_modules e .git
            dirs[:] = [d for d in dirs if d not in ["node_modules", ".git", "__pycache__"]]
            level = root.replace(self.repo_root, "").count(os.sep)
            structure.append({
                "path": root.replace(self.repo_root, ""),
                "level": level,
                "files": files
            })
        return structure

    def get_readme(self):
        readme_path = os.path.join(self.repo_root, "README.md")
        if not os.path.exists(readme_path):
            return ""
        with open(readme_path, "r", encoding="utf-8") as f:
            return f.read()

    def get_recent_commits(self, limit=5):
        try:
            output = subprocess.check_output(
                ["git", "log", f"-{limit}", "--pretty=format:%h|%an|%ad|%s"],
                cwd=self.repo_root,
                text=True
            )
            commits = []
            for line in output.splitlines():
                h, author, date, msg = line.split("|", 3)
                commits.append({
                    "hash": h,
                    "author": author,
                    "date": date,
                    "message": msg
                })
            return commits
        except Exception:
            return []

    def collect(self):
        context = {
            "collected_at": datetime.now(timezone.utc).isoformat(),
            "repo_structure": self.get_repo_structure(),
            "readme": self.get_readme(),
            "recent_commits": self.get_recent_commits(),
        }
        return context


if __name__ == "__main__":
    collector = ContextCollector(repo_root=".")
    ctx = collector.collect()
    print(json.dumps(ctx, indent=2, ensure_ascii=False))

