cd ~/portfolio-silas
claude "Leia todos os arquivos em ai/ antes de qualquer coisa:
- ai/README.md
- ai/core/model_router.py
- ai/scripts/llm_client.py
- ai/scripts/context_collector.py
- ai/scripts/run_all.py
- ai/agents/update_bio.py
- ai/prompts/update_bio.md
- todos os outros agents e prompts

Depois implemente as seguintes mudanças:

1. ai/scripts/llm_client.py
   - Adicionar suporte a LLM_PROVIDER=anthropic
   - Usar SDK anthropic versão 0.86.0 já instalado
   - ANTHROPIC_API_KEY lida do ambiente
   - Modelos: claude-sonnet-4-5 para short_text/analysis, claude-opus-4-5 para long_markdown
   - Fallback automático para OpenAI se ANTHROPIC_API_KEY ausente
   - Logar provider e modelo usado em cada chamada

2. ai/core/model_router.py
   - Refatorar MODEL_BY_TASK para dual-provider:
     {'openai': {'short_text': 'gpt-4o-mini', 'long_markdown': 'gpt-4o-mini', 'analysis': 'gpt-4o-mini'},
      'anthropic': {'short_text': 'claude-sonnet-4-5', 'long_markdown': 'claude-opus-4-5', 'analysis': 'claude-sonnet-4-5'}}
   - Função get_model(task, provider) para roteamento limpo

3. ai/scripts/test_anthropic.py (arquivo novo)
   - Teste: gera bio curta com claude-sonnet-4-5
   - Printa provider, modelo, tempo de resposta e output

4. ai/agents/update_bio.py
   - Logar provider e modelo após geração

5. ai/README.md
   - Seção Providers com OpenAI e Anthropic
   - Variáveis: LLM_PROVIDER, LLM_API_KEY, ANTHROPIC_API_KEY

6. atualize o CHANGELOG.md

Um commit por arquivo. Mensagens em inglês com co-author:
Co-authored-by: Claude Sonnet <claude@anthropic.com>"