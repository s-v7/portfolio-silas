# Relatório da Rede Neural - Análise do Ecossistema

**Total de Projetos e Evidências Mapeadas:** 150

## Distribuição por Categoria de Software

| Categoria | Qtd. Projetos | Proporção (%) |
| :--- | :---: | :---: |
| `ai-mcp-llm` | 40 | 26.67% |
| `backend-python` | 2 | 1.33% |
| `backend-java-enterprise` | 36 | 24.00% |
| `frontend-node-ts` | 14 | 9.33% |
| `systems-c-shell` | 26 | 17.33% |
| `infra-db-tools` | 5 | 3.33% |
| `finance-tools` | 4 | 2.67% |
| `general-dev` | 23 | 15.33% |

## Arquitetura da Rede Neural (PyTorch MLP)
- **Entrada:** Vetorização TF-IDF (Unigramas e Bigramas, 500 features).
- **Camadas Ocultas:** `Linear(500, 128)` -> `BatchNorm1d` -> `ReLU` -> `Dropout(0.3)` -> `Linear(128, 64)` -> `ReLU`.
- **Camada de Saída:** `Linear(64, num_classes)` com Perda Cross-Entropy.
- **Otimizador:** AdamW (Learning Rate: 0.008, Weight Decay: 0.01).

---
*Relatório gerado automaticamente pelo pipeline de IA do Portfolio Silas.*
