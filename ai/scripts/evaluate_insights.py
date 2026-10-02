from __future__ import annotations

import json
import pickle
import re
from pathlib import Path
from typing import Any

import torch
import torch.nn as nn

DATASET_PATH = Path("ai/data/dataset_evidence.jsonl")
MODEL_DIR = Path("ai/models")
MODEL_PATH = MODEL_DIR / "ecosystem_classifier.pt"
VECTORIZER_PATH = MODEL_DIR / "tfidf_vectorizer.pkl"
CATEGORIES_PATH = MODEL_DIR / "category_mapping.json"
REPORT_OUTPUT_PATH = Path("ai/data/ecosystem_insights.json")


def clean_text(text: str) -> str:
    text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)
    text = re.sub(r"https?://\S+", "", text)
    text = re.sub(r"[^\w\s\-\.]", " ", text)
    return text.lower().strip()


class EcosystemMLP(nn.Module):
    """Arquitetura sincronizada com o train_neural_net.py (128 -> 64 -> num_classes)."""

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


def load_artifacts() -> tuple[EcosystemMLP, Any, dict[int, str]]:
    if not MODEL_PATH.exists() or not VECTORIZER_PATH.exists() or not CATEGORIES_PATH.exists():
        raise FileNotFoundError("Artefatos do modelo não encontrados. Treine a rede primeiro.")

    with VECTORIZER_PATH.open("rb") as f:
        vectorizer = pickle.load(f)

    with CATEGORIES_PATH.open("r", encoding="utf-8") as f:
        category_to_idx: dict[str, int] = json.load(f)
        idx_to_category = {v: k for k, v in category_to_idx.items()}

    input_dim = len(vectorizer.get_feature_names_out())
    num_classes = len(category_to_idx)

    model = EcosystemMLP(input_dim, num_classes)
    model.load_state_dict(torch.load(MODEL_PATH, weights_only=True))
    model.eval()

    return model, vectorizer, idx_to_category


def evaluate_ecosystem() -> None:
    print("[1/3] Carregando modelo e vetorizador...")
    model, vectorizer, idx_to_category = load_artifacts()

    if not DATASET_PATH.exists():
        raise FileNotFoundError(f"Dataset '{DATASET_PATH}' não encontrado.")

    print("[2/3] Deduplicando dataset e executando inferência...")
    project_results: list[dict[str, Any]] = []
    category_counts: dict[str, int] = {cat: 0 for cat in idx_to_category.values()}

    # Deduplicação por 'identifier' (mantém o registro mais recente)
    unique_items: dict[str, dict[str, Any]] = {}
    with DATASET_PATH.open("r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            item = json.loads(line)
            identifier = item.get("identifier")
            if identifier:
                unique_items[identifier] = item

    print(f"      Total de registros únicos analisados: {len(unique_items)}")

    for identifier, item in unique_items.items():
        content_clean = clean_text(item.get("content", ""))
        path_str = item.get("source_path", "")
        full_context = f"{identifier} {content_clean} {path_str}"

        X_tfidf = vectorizer.transform([full_context]).toarray()
        X_tensor = torch.tensor(X_tfidf, dtype=torch.float32)

        with torch.no_grad():
            outputs = model(X_tensor)
            probabilities = torch.softmax(outputs, dim=1)
            confidence, predicted_idx = torch.max(probabilities, 1)

        predicted_category = idx_to_category[predicted_idx.item()]
        conf_score = round(confidence.item() * 100, 2)

        category_counts[predicted_category] += 1

        project_results.append(
            {
                "identifier": identifier,
                "source_path": path_str,
                "predicted_category": predicted_category,
                "confidence_percentage": conf_score,
            }
        )

    total_evidences = len(project_results)
    distribution = {
        cat: {
            "count": count,
            "percentage": round((count / total_evidences) * 100, 2) if total_evidences > 0 else 0,
        }
        for cat, count in category_counts.items()
    }

    report = {
        "total_unique_evidences": total_evidences,
        "ecosystem_distribution": distribution,
        "classifications": project_results,
    }

    REPORT_OUTPUT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print("\n" + "=" * 60)
    print("      RELATÓRIO DE INSIGHTS DO ECOSSISTEMA (DEDUPLICADO)")
    print("=" * 60)
    print(f"Total de evidências únicas: {total_evidences}\n")
    print("Distribuição das Competências:")
    for cat, data in distribution.items():
        bar = "█" * int(data["percentage"] / 5)
        print(f"  • {cat:<24} | {data['percentage']:>6.2f}% ({data['count']:>2} proj) {bar}")

    print("\nExemplo de Classificações:")
    for proj in project_results[:5]:
        print(f"  ✓ {proj['identifier']} -> {proj['predicted_category']} ({proj['confidence_percentage']}%)")

    print(f"\n[Sucesso] Relatório salvo em '{REPORT_OUTPUT_PATH}'.")


if __name__ == "__main__":
    evaluate_ecosystem()
