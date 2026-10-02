from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

EVIDENCE_JSON_PATH = Path("ai/data/portfolio_evidence.json")
DATASET_JSONL_PATH = Path("ai/data/dataset_evidence.jsonl")

IGNORE_DIRS = {
    ".git",
    "node_modules",
    "__pycache__",
    ".venv",
    "venv",
    "houseVenv",
    "venvHouse",
    ".idea",
    ".vscode",
    "dist",
    "build",
    "target",
}


def sanitize_identifier(path: Path) -> str:
    """Gera um identificador limpo e padronizado para o diretório."""
    name = path.name if path.name else "root"
    clean_name = re.sub(r"[^\w\-]", "_", name).lower()
    return f"local-{clean_name}"


def summarize_directory_structure(dir_path: Path) -> str:
    """Para pastas sem README, gera um resumo textual da estrutura de arquivos para servir de evidência."""
    extensions: set[str] = set()
    sample_files: list[str] = []

    try:
        for item in dir_path.rglob("*"):
            if any(part in IGNORE_DIRS for part in item.parts):
                continue
            if item.is_file():
                if item.suffix:
                    extensions.add(item.suffix.lower())
                if len(sample_files) < 15:
                    sample_files.append(item.name)
    except Exception:
        pass

    ext_str = ", ".join(sorted(extensions)[:10])
    files_str = ", ".join(sample_files)

    return f"Diretório: {dir_path.name}. Extensões detectadas: [{ext_str}]. Arquivos no projeto: [{files_str}]."


def extract_evidence_from_dir(dir_path: Path) -> list[dict[str, Any]]:
    """Extrai evidências textuais de um diretório de projeto."""
    evidences: list[dict[str, Any]] = []

    # Tenta localizar arquivos de documentação prioritários
    doc_files = list(dir_path.glob("README*")) + list(dir_path.glob("CHANGELOG*"))
    has_docs = False

    for doc_file in doc_files:
        if doc_file.is_file() and doc_file.stat().st_size > 0:
            try:
                content = doc_file.read_text(encoding="utf-8", errors="ignore")
                doc_type = doc_file.stem.lower()
                identifier = f"{sanitize_identifier(dir_path)}-{doc_type}"

                evidences.append(
                    {
                        "identifier": identifier,
                        "type": f"local_{doc_type}",
                        "source_path": str(doc_file.resolve()),
                        "content": content[:4000],  # Limita tamanho para contextualização eficaz
                    }
                )
                has_docs = True
            except Exception as e:
                print(f"Erro lendo {doc_file}: {e}")

    # Se não houver README/CHANGELOG, cria evidência sintética estrutural
    if not has_docs:
        identifier = f"{sanitize_identifier(dir_path)}-struct"
        summary = summarize_directory_structure(dir_path)
        evidences.append(
            {
                "identifier": identifier,
                "type": "local_structure_synth",
                "source_path": str(dir_path.resolve()),
                "content": summary,
            }
        )

    return evidences


def discover_projects(roots: list[Path]) -> list[Path]:
    """Descobre projetos e diretórios em raízes especificadas."""
    discovered: set[Path] = set()

    for root in roots:
        if not root.exists():
            print(f" Caminho '{root}' não existe. Ignorando...")
            continue

        if root.is_file():
            continue

        # Se a própria pasta for um projeto ou repositório
        if (root / ".git").exists() or any(root.glob("README*")) or any(root.glob("pom.xml")) or any(root.glob("requirements.txt")):
            discovered.add(root.resolve())
            continue

        # Varre o subdiretório em busca de projetos
        print(f" Escaneando diretório raiz: {root}")
        try:
            for item in root.iterdir():
                if item.is_dir() and item.name not in IGNORE_DIRS and not item.name.startswith("."):
                    discovered.add(item.resolve())
        except Exception as e:
            print(f" Erro ao acessar subpastas de '{root}': {e}")

    return sorted(list(discovered))


def run_extraction(target_dirs: list[str]) -> None:
    print("[1/3] Identificando diretórios e projetos...")
    root_paths = [Path(d).expanduser().resolve() for d in target_dirs]
    projects = discover_projects(root_paths)

    print(f"Total de diretórios/projetos identificados: {len(projects)}")

    print("[2/3] Extraindo evidências dos diretórios...")
    all_evidences: list[dict[str, Any]] = []

    for proj in projects:
        evs = extract_evidence_from_dir(proj)
        all_evidences.extend(evs)
        print(f"{proj.name:<35} | {len(evs)} evidência(s) capturada(s)")

    print(f"\n[3/3] Atualizando dataset e histórico acumulativo...")
    
    # 1. Salva foto atual do portfólio
    EVIDENCE_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    EVIDENCE_JSON_PATH.write_text(json.dumps(all_evidences, ensure_ascii=False, indent=2), encoding="utf-8")

    # 2. Atualiza o dataset .jsonl acumulativo (deduplicando por identifier)
    existing_records: dict[str, dict[str, Any]] = {}
    if DATASET_JSONL_PATH.exists():
        with DATASET_JSONL_PATH.open("r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    item = json.loads(line)
                    if "identifier" in item:
                        existing_records[item["identifier"]] = item

    # Adiciona/Atualiza novas evidências
    for ev in all_evidences:
        existing_records[ev["identifier"]] = ev

    # Grava dataset unificado
    with DATASET_JSONL_PATH.open("w", encoding="utf-8") as f:
        for record in existing_records.values():
            f.write(json.json_dumps(record, ensure_ascii=False) + "\n") if hasattr(json, "json_dumps") else f.write(json.dumps(record, ensure_ascii=False) + "\n")

    print("\n" + "=" * 60)
    print(f"  EXTRAÇÃO CONCLUÍDA COM SUCESSO!")
    print(f"  Evidências da sessão: {len(all_evidences)}")
    print(f"  Total no dataset (.jsonl): {len(existing_records)}")
    print(f"  Arquivo acumulativo: {DATASET_JSONL_PATH}")
    print("=" * 60)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extração universal de evidências para todos os 83 projetos.")
    parser.add_argument(
        "--dir",
        nargs="+",
        default=["."],
        help="Diretórios locais ou raízes onde estão armazenados os seus projetos.",
    )
    args = parser.parse_args()

    run_extraction(args.dir)
