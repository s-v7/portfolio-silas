from __future__ import annotations

import json
import pickle
import re
from pathlib import Path
from typing import Any

import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.feature_extraction.text import TfidfVectorizer
from torch.utils.data import DataLoader, Dataset

DATASET_PATH = Path("ai/data/dataset_evidence.jsonl")
MODEL_DIR = Path("ai/models")
MODEL_PATH = MODEL_DIR / "ecosystem_classifier.pt"
VECTORIZER_PATH = MODEL_DIR / "tfidf_vectorizer.pkl"
CATEGORIES_PATH = MODEL_DIR / "category_mapping.json"

CATEGORIES = [
    "ai-mcp-llm",
    "backend-python",
    "backend-java-enterprise",
    "frontend-node-ts",
    "systems-c-shell",
    "infra-db-tools",
    "finance-tools",
    "general-dev",
]


def clean_text(text: str) -> str:
    """Remove URLs Markdown e caracteres especiais mantendo termos técnicos."""
    text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)
    text = re.sub(r"https?://\S+", "", text)
    text = re.sub(r"[^\w\s\-\.]", " ", text)
    return text.lower().strip()


def heuristic_labeling(identifier: str, content: str, source_path: str = "") -> str:
    """Taxonomia ajustada para priorizar nomes de repositórios/projetos e contexto exato."""
    ident = identifier.lower()
    text = f"{identifier} {content} {source_path}".lower()

    # Overrides explícitos para o repositório central do portfólio
    if "portfolio-silas" in ident or "portfolio-silas" in text:
        return "ai-mcp-llm"

    # AI, LLMs e MCP
    if any(k in text for k in ["mcp", "llm", "agent", "neural", "art-analysis", "model-spinning", "creapi-ai", "phantom-search", "machine-learning"]):
        return "ai-mcp-llm"

    # Java & Forense Corporativa (Ancoragem forte em Java / Jakarta / GlassFish)
    if any(k in text for k in ["iped", "glassfish", "payara", "netbeans", "sistemacrea", "ru-creapi", "jakarta", "java"]):
        return "backend-java-enterprise"

    # Frontend JS/TS / Web
    if any(k in text for k in ["react", "nextjs", "typescript", "rufrontend", "portfolio-silas", "frontend", "vue", "node"]):
        return "frontend-node-ts"

    # C, Shell & Baixo Nível
    if any(k in text for k in ["ponteiros", "sleuthkit", "patch", "refactor_sigec", "shell", ".sh", ".c"]):
        return "systems-c-shell"

    # Infra, DBs, Venvs e Dumps
    if any(k in text for k in ["db", "dump", "venv", "schema", "migration", "postgres", "mysql"]):
        return "infra-db-tools"

    # Ferramentas Financeiras
    if any(k in text for k in ["finance", "financeira", "calculadora", "cal_"]):
        return "finance-tools"

    # Backend Python
    if any(k in text for k in ["fastapi", "flask", "django", "crea-fastapi", "trojan", "lotto", "python"]):
        return "backend-python"

    return "general-dev"


class TextDataset(Dataset):
    def __init__(self, X_tensor: torch.Tensor, y_tensor: torch.Tensor):
        self.X = X_tensor
        self.y = y_tensor

    def __len__(self) -> int:
        return len(self.y)

    def __getitem__(self, idx: int) -> tuple[torch.Tensor, torch.Tensor]:
        return self.X[idx], self.y[idx]


class EcosystemMLP(nn.Module):
    def __init__(self, input_dim: int, num_classes: int):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(input_dim, 128),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, num_classes),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.network(x)


def load_data() -> tuple[list[str], list[int], dict[str, int]]:
    if not DATASET_PATH.exists():
        raise FileNotFoundError(f"Dataset não encontrado em '{DATASET_PATH}'. Execute a extração primeiro.")

    unique_items: dict[str, dict[str, Any]] = {}
    with DATASET_PATH.open("r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            item = json.loads(line)
            identifier = item.get("identifier")
            if identifier:
                unique_items[identifier] = item

    texts: list[str] = []
    labels_raw: list[str] = []

    for identifier, item in unique_items.items():
        content_clean = clean_text(item.get("content", ""))
        path_str = item.get("source_path", "")

        full_context = f"{identifier} {content_clean} {path_str}"
        label = heuristic_labeling(identifier, content_clean, path_str)

        texts.append(full_context)
        labels_raw.append(label)

    label_to_idx = {cat: idx for idx, cat in enumerate(CATEGORIES)}
    y = [label_to_idx[lbl] for lbl in labels_raw]

    return texts, y, label_to_idx

def train() -> None:
    print("[1/5] Carregando dataset e aplicando taxonomia expandida...")
    texts, y, label_to_idx = load_data()
    print(f"      Total de exemplos carregados: {len(texts)}")

    print("[2/5] Vetorizando contexto textual com TF-IDF...")
    vectorizer = TfidfVectorizer(max_features=500, ngram_range=(1, 2))
    X_tfidf = vectorizer.fit_transform(texts).toarray()

    X_tensor = torch.tensor(X_tfidf, dtype=torch.float32)
    y_tensor = torch.tensor(y, dtype=torch.long)

    dataset = TextDataset(X_tensor, y_tensor)
    dataloader = DataLoader(dataset, batch_size=4, shuffle=True)

    print("[3/5] Inicializando Rede Neural MLP Expandida...")
    input_dim = X_tfidf.shape[1]
    num_classes = len(CATEGORIES)
    model = EcosystemMLP(input_dim=input_dim, num_classes=num_classes)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.AdamW(model.parameters(), lr=0.008, weight_decay=0.01)

    print("[4/5] Treinando modelo...")
    model.train()
    epochs = 35
    for epoch in range(1, epochs + 1):
        total_loss = 0.0
        correct = 0
        total = 0

        for batch_X, batch_y in dataloader:
            optimizer.zero_grad()
            outputs = model(batch_X)
            loss = criterion(outputs, batch_y)
            loss.backward()
            optimizer.step()

            total_loss += loss.item() * batch_X.size(0)
            _, predicted = torch.max(outputs, 1)
            total += batch_y.size(0)
            correct += (predicted == batch_y).sum().item()

        acc = (correct / total) * 100
        avg_loss = total_loss / total
        if epoch % 10 == 0 or epoch == epochs:
            print(f"      Época {epoch:02d}/{epochs} | Perda: {avg_loss:.4f} | Acurácia: {acc:.1f}%")

    print("[5/5] Salvando modelo e vocabulário...")
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    torch.save(model.state_dict(), MODEL_PATH)

    with VECTORIZER_PATH.open("wb") as f:
        pickle.dump(vectorizer, f)

    with CATEGORIES_PATH.open("w", encoding="utf-8") as f:
        json.dump(label_to_idx, f, indent=2)

    print("\n[Sucesso] Treinamento com taxonomia de 83 projetos concluído!")


if __name__ == "__main__":
    train()
