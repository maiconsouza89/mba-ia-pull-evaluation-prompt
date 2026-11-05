"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.

Este script:
1. Lê os prompts otimizados de prompts/bug_to_user_story_v2.yml
2. Valida os prompts
3. Faz push PÚBLICO para o LangSmith Hub
4. Adiciona metadados (tags, descrição, técnicas utilizadas)

DICAS DE IMPLEMENTAÇÃO:

- O push é feito pelo cliente do LangSmith:

      from langsmith import Client
      from langchain_core.prompts import ChatPromptTemplate

      client = Client()
      prompt = ChatPromptTemplate.from_messages([
          ("system", system_prompt),
          ("user", user_prompt),
      ])
      url = client.push_prompt(
          f"{username}/bug_to_user_story_v2",
          object=prompt,
          is_public=True,
          description="...",
          tags=[...],
      )

- `username` vem de USERNAME_LANGSMITH_HUB no .env e precisa ser o seu handle
  do Hub. Se você ainda não tem um handle, veja as instruções no .env.example.

- A variável do template precisa ser {bug_report}, que é a chave de entrada
  usada no dataset de avaliação.

- Use `load_yaml` de utils.py para ler o arquivo .yml.
"""

import os
import sys
from dotenv import load_dotenv
from langsmith import Client
from langchain_core.prompts import ChatPromptTemplate
from utils import load_yaml, check_env_vars, print_section_header, validate_prompt_structure

load_dotenv()


def push_prompt_to_langsmith(prompt_name: str, prompt_data: dict) -> bool:
    """
    Faz push do prompt otimizado para o LangSmith Hub (PÚBLICO).

    Args:
        prompt_name: Nome do prompt
        prompt_data: Dados do prompt

    Returns:
        True se sucesso, False caso contrário
    """
    try:
        client = Client()

        system_prompt = prompt_data.get('system_prompt', '')
        user_prompt = prompt_data.get('user_prompt', '')

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("user", user_prompt),
        ])

        description = prompt_data.get('description', '')
        tags = prompt_data.get('tags', [])

        url = client.push_prompt(
            prompt_name,
            object=prompt,
            is_public=True,
            description=description,
            tags=tags,
        )

        print(
            f"✅ Prompt '{prompt_name}' enviado com sucesso para o LangSmith Hub!")
        print(f"URL do prompt: {url}")
        return True

    except Exception as e:
        print(f"❌ Erro ao fazer push do prompt: {e}")
        return False


def validate_prompt(prompt_data: dict) -> tuple[bool, list]:
    """
    Valida estrutura básica de um prompt (versão simplificada).

    Args:
        prompt_data: Dados do prompt

    Returns:
        (is_valid, errors) - Tupla com status e lista de erros
    """
    _, errors = validate_prompt_structure(prompt_data)

    if 'user_prompt' not in prompt_data or not prompt_data['user_prompt'].strip():
        errors.append("user_prompt está vazio ou ausente")
    elif '{bug_report}' not in prompt_data['user_prompt']:
        errors.append("user_prompt deve conter a variável {bug_report}")

    return (len(errors) == 0, errors)


def main():
    """Função principal"""
    print_section_header("PUSH DE PROMPTS PARA O LANGSMITH HUB")

    required_env_vars = ["USERNAME_LANGSMITH_HUB", "LANGSMITH_API_KEY"]
    if not check_env_vars(required_env_vars):
        return 1

    yaml_data = load_yaml("prompts/bug_to_user_story_v2.yml")

    if not yaml_data:
        print("❌ Erro ao carregar dados do prompt")
        return 1

    # O YAML guarda o conteúdo sob a chave com o nome do prompt
    prompt_data = yaml_data.get("bug_to_user_story_v2")

    if not prompt_data:
        print("❌ Chave 'bug_to_user_story_v2' não encontrada no YAML")
        return 1

    is_valid, errors = validate_prompt(prompt_data)

    if not is_valid:
        print(f"❌ Erros de validação: {errors}")
        return 1

    prompt_name = f"{os.getenv('USERNAME_LANGSMITH_HUB')}/bug_to_user_story_v2"

    success = push_prompt_to_langsmith(prompt_name, prompt_data)

    if not success:
        print("❌ Falha ao fazer push do prompt para o LangSmith Hub")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
