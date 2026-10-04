from __future__ import annotations

import json
from pathlib import Path

INSIGHTS_PATH = Path("ai/data/ecosystem_insights.json")
DASHBOARD_HTML_PATH = Path("ai/data/dashboard.html")


def generate_html_dashboard() -> None:
    if not INSIGHTS_PATH.exists():
        raise FileNotFoundError(f"Arquivo '{INSIGHTS_PATH}' não encontrado. Execute evaluate_insights primeiro.")

    data = json.loads(INSIGHTS_PATH.read_text(encoding="utf-8"))
    distribution = data.get("ecosystem_distribution", {})
    total = data.get("total_unique_evidences", 0)

    labels = list(distribution.keys())
    counts = [d["count"] for d in distribution.values()]
    percentages = [d["percentage"] for d in distribution.values()]

    html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard do Ecossistema - Portfolio Silas</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #0f172a;
            color: #f8fafc;
            margin: 0;
            padding: 20px;
        }}
        .container {{
            max-width: 1000px;
            margin: 0 auto;
        }}
        h1 {{
            color: #38bdf8;
            text-align: center;
        }}
        .card {{
            background-color: #1e293b;
            border-radius: 12px;
            padding: 24px;
            margin-top: 20px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
        }}
        .metric-title {{
            font-size: 1.1rem;
            color: #94a3b8;
        }}
        .metric-value {{
            font-size: 2.5rem;
            font-weight: bold;
            color: #38bdf8;
        }}
        canvas {{
            max-height: 400px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🌌 Visão do Ecossistema (ML Neural Classifier)</h1>
        
        <div class="card">
            <div class="metric-title">Total de Projetos & Evidências Analisadas</div>
            <div class="metric-value">{total}</div>
        </div>

        <div class="card">
            <canvas id="ecosystemChart"></canvas>
        </div>
    </div>

    <script>
        const ctx = document.getElementById('ecosystemChart').getContext('2d');
        new Chart(ctx, {{
            type: 'bar',
            data: {{
                labels: {json.dumps(labels)},
                datasets: [{{
                    label: 'Quantidade de Projetos',
                    data: {json.dumps(counts)},
                    backgroundColor: [
                        '#38bdf8', '#818cf8', '#c084fc', '#f472b6',
                        '#fb7185', '#34d399', '#fbbf24', '#94a3b8'
                    ],
                    borderWidth: 1
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{ display: false }},
                    title: {{
                        display: true,
                        text: 'Distribuição de Competências por Categoria',
                        color: '#f8fafc',
                        font: {{ size: 16 }}
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        ticks: {{ color: '#94a3b8' }},
                        grid: {{ color: '#334155' }}
                    }},
                    x: {{
                        ticks: {{ color: '#94a3b8' }},
                        grid: {{ display: false }}
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>
"""

    DASHBOARD_HTML_PATH.write_text(html_content, encoding="utf-8")
    print(f"[Sucesso] Dashboard HTML exportado para: '{DASHBOARD_HTML_PATH}'")


if __name__ == "__main__":
    generate_html_dashboard()
