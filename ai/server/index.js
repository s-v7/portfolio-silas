import express from "express";
import cors from "cors";
import dotenv from "dotenv";
import path from "path";
import { fileURLToPath } from "url";

import { askOpenAI } from "../providers/openai.js";
import { askAnthropic } from "../providers/anthropic.js";
import { askNvidia } from "../providers/nvidia.js";

import { buildCareerPrompt  } from "../services/PromptBuilder.js";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

dotenv.config({
  path: path.resolve(__dirname, "../../.env"),
});

console.log("ENV loaded:", {
  openai: Boolean(process.env.OPENAI_API_KEY),
  anthropic: Boolean(process.env.ANTHROPIC_API_KEY),
  nvidia: Boolean(process.env.NVIDIA_API_KEY),
});

const app = express();

app.use(cors());
app.use(express.json());

app.get("/api/health", (req, res) => {
  res.json({ ok: true, service: "ai-server" });
});

app.post("/api/chat", async (req, res) => {
  try {
    const { message, provider = process.env.AI_PROVIDER || "openai", mode = "career" } = req.body;

    if (!message) {
      return res.status(400).json({ error: "message is required" });
    }

    const finalMessage = 
      mode === "career"
        ? buildCareerPrompt(message)
	: message;

    let answer;

    if (provider === "openai") {
      answer = await askOpenAI(finalMessage);
    } else if (provider === "anthropic") {
      answer = await askAnthropic(finalMessage);
    } else if (provider === "nvidia") {
      answer = await askNvidia(finalMessage);
    } else {
      return res.status(400).json({ error: "invalid provider" });
    }

    res.json({ provider, answer });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "AI request failed" });
  }
});

const port = process.env.PORT || 3333;

app.listen(port, () => {
  console.log(`AI server running on port ${port}`);
});
