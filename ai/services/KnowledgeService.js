import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const KNOWLEDGE_DIR = path.resolve(__dirname, "../knowledge");

export function loadKnowledgeBase() {
  const files = ["cv.md", "experience.md", "skills.md", "education.md"];
  return files
    .map((file) => {
      const fullPath = path.join(KNOWLEDGE_DIR, file);
      return fs.existsSync(fullPath) ? fs.readFileSync(fullPath, "utf-8") : "";
    })
    .filter(Boolean)
    .join("\n\n---\n\n");
}
