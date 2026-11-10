# Como Executar

## Pré-requisitos

- Python 3.10+
- Conta no LangSmith com API key e handle público do Hub ([como criar](../README.md#handle-do-langsmith-hub-seu-username))
- API key de um provider de LLM: OpenAI, Google ou Anthropic

## Instalação

```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

No `.env`, preencha:

- `LANGSMITH_API_KEY`, `LANGSMITH_PROJECT` e `USERNAME_LANGSMITH_HUB`
- `LLM_PROVIDER` (`openai`, `google` ou `anthropic`) e a chave correspondente
- `LLM_MODEL` e `EVAL_MODEL`

Na entrega foram usados `anthropic`, `claude-haiku-5-5` e `claude-sonnet-5-5`.

### Provider Anthropic (adicionado nesta entrega)

O projeto base suportava apenas OpenAI e Google. Para usar os modelos Claude, foi incluído o provider `anthropic`:

| Arquivo | Alteração |
|---|---|
| `src/utils.py` | `get_llm()` cria um `ChatAnthropic` quando `LLM_PROVIDER=anthropic` |
| `requirements.txt` | Pacotes `anthropic` e `langchain-anthropic` |
| `.env.example` | Variável `ANTHROPIC_API_KEY` e `anthropic` na lista de providers |

Para usar: `LLM_PROVIDER=anthropic`, `ANTHROPIC_API_KEY` com uma chave do [Console da Anthropic](https://console.anthropic.com/) e `LLM_MODEL`/`EVAL_MODEL` com modelos Claude.

## Fases

| Fase | Comando | O que faz |
|---|---|---|
| 1. Pull | `python src/pull_prompts.py` | Baixa o prompt original para `prompts/bug_to_user_story_v1.yml` |
| 2. Otimização | editar `prompts/bug_to_user_story_v2.yml` | Aplica as técnicas de prompt engineering |
| 3. Testes | `pytest tests/test_prompts.py -v` | Valida a estrutura do prompt |
| 4. Push | `python src/push_prompts.py` | Publica o v2 no LangSmith Hub |
| 5. Avaliação | `python src/evaluate.py` | Roda o v2 no dataset e mostra as 5 métricas (aprovado se todas ≥ 0.8) |

Se alguma métrica ficar abaixo de 0.8, leia os comentários dos juízes no experimento do LangSmith, ajuste o prompt e repita as fases 3 a 5.
