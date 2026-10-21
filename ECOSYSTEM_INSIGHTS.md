# Relatório da Rede Neural - Análise do Ecossistema

**Evidências analisadas (README e CHANGELOG):** 87

63 resumos de pasta ficaram de fora: eles listam só extensões e nomes de arquivo.

## Distribuição por Categoria de Software

As categorias são heurísticas (regras sobre o texto), não uma classificação verificada.

| Categoria | Qtd. Evidências | Proporção (%) |
| :--- | :---: | :---: |
| `ai-mcp-llm` | 31 | 35.63% |
| `backend-python` | 1 | 1.15% |
| `backend-java-enterprise` | 17 | 19.54% |
| `frontend-node-ts` | 16 | 18.39% |
| `systems-c-shell` | 5 | 5.75% |
| `infra-db-tools` | 2 | 2.30% |
| `finance-tools` | 2 | 2.30% |
| `general-dev` | 13 | 14.94% |

## Avaliação

- **Acurácia em dados separados:** 61.1% (18 exemplos de teste)
- **Linha de base (sempre a classe mais comum):** 38.9%
- Os rótulos vêm de uma regra, então a acurácia mede o quanto a rede imita a regra, não a verdade sobre os projetos.

## Arquitetura da Rede Neural (PyTorch MLP)
- **Entrada:** Vetorização TF-IDF (Unigramas e Bigramas, 500 features).
- **Camadas Ocultas:** `Linear(500, 128)` -> `BatchNorm1d` -> `ReLU` -> `Dropout(0.3)` -> `Linear(128, 64)` -> `ReLU`.
- **Camada de Saída:** `Linear(64, num_classes)` com Perda Cross-Entropy.
- **Otimizador:** AdamW (Learning Rate: 0.008, Weight Decay: 0.01).

---
*Relatório gerado automaticamente pelo pipeline de IA do Portfolio Silas.*
