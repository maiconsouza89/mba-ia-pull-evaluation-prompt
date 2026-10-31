"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull do prompt semente do desafio
3. Salva localmente em prompts/bug_to_user_story_v1.yml

DICAS DE IMPLEMENTAÇÃO:

- O pull é feito pelo cliente do LangSmith:

      from langsmith import Client
      client = Client()
      prompt = client.pull_prompt(
          "leonanluppi/bug_to_user_story_v1",
          dangerously_pull_public_prompt=True,
      )

- O parâmetro `dangerously_pull_public_prompt=True` é obrigatório sempre que o
  identificador tem dono explícito ("owner/nome"). O LangSmith bloqueia esse pull
  por padrão porque um prompt do Hub é um objeto LangChain serializado, que pode
  vir de terceiros. Aqui o prompt é o do desafio, então o risco é conhecido.

- O retorno é um ChatPromptTemplate. Para extrair o conteúdo das mensagens,
  use a serialização nativa do LangChain (`prompt.messages`, e o atributo
  `.prompt.template` de cada mensagem).

- Use `save_yaml` de utils.py para gravar o resultado no arquivo .yml.
"""

from langchain_core.prompts import HumanMessagePromptTemplate, SystemMessagePromptTemplate
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from langsmith import Client
from utils import save_yaml, check_env_vars, print_section_header

load_dotenv()


PROMPT_ID = "leonanluppi/bug_to_user_story_v1"
PROMPT_KEY = "bug_to_user_story_v1"
OUTPUT_PATH = "prompts/bug_to_user_story_v1.yml"


def pull_prompts_from_langsmith():
    """Faz pull do prompt no Hub e retorna um dict com conteúdo e metadados."""
    client = Client()
    prompt = client.pull_prompt(PROMPT_ID, dangerously_pull_public_prompt=True)
    info = client.get_prompt(PROMPT_ID)

    system_prompt, user_prompt = "", ""
    for msg in prompt.messages:
        if isinstance(msg, SystemMessagePromptTemplate):
            system_prompt = msg.prompt.template
        elif isinstance(msg, HumanMessagePromptTemplate):
            user_prompt = msg.prompt.template

    meta = prompt.metadata or {}

    print(meta)
    print(info)
    return {
        PROMPT_KEY: {
            "description": getattr(info, "description", None),
            "system_prompt": system_prompt,
            "user_prompt": user_prompt,
            "version": getattr(info, "version", None) or "v1",
            "tags": list(getattr(info, "tags", None) or []),
        }
    }


def main():
    """Função principal"""
    print_section_header("Pull do prompt do LangSmith")

    if not check_env_vars(["LANGSMITH_API_KEY"]):
        return 1

    try:
        data = pull_prompts_from_langsmith()
    except Exception as e:
        print(f"❌ Erro ao fazer pull de {PROMPT_ID}: {e}")
        return 1

    if not save_yaml(data, OUTPUT_PATH):
        return 1

    print(f"✅ Prompt salvo em {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
