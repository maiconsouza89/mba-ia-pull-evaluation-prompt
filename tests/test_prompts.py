"""
Testes automatizados para validação de prompts.
"""
import re
import pytest
import yaml
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils import validate_prompt_structure

def load_prompts(file_path: str):
    """Carrega prompts do arquivo YAML."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


PROMPT_FILE = Path(__file__).parent.parent / "prompts" / "bug_to_user_story_v2.yml"
PROMPT_KEY = "bug_to_user_story_v2"


@pytest.fixture
def prompt():
    """Retorna o dicionário interno do prompt (já sem a chave raiz)."""
    data = load_prompts(PROMPT_FILE)
    assert PROMPT_KEY in data, f"Chave '{PROMPT_KEY}' não encontrada no YAML"
    return data[PROMPT_KEY]


class TestPrompts:
    def test_prompt_has_system_prompt(self, prompt):
        """Verifica se o campo 'system_prompt' existe e não está vazio."""
        assert "system_prompt" in prompt, "Campo 'system_prompt' ausente"
        assert prompt["system_prompt"].strip(), "'system_prompt' está vazio"

    def test_prompt_has_role_definition(self, prompt):
        """Verifica se o prompt define uma persona (ex: "Você é um Product Manager")."""
        assert re.search(r"voc[eê] [eé] uma?\s", prompt["system_prompt"], re.IGNORECASE), \
            "Nenhuma persona definida (ex: 'Você é um Product Manager')"

    def test_prompt_mentions_format(self, prompt):
        """Verifica se o prompt exige formato Markdown ou User Story padrão."""
        text = prompt["system_prompt"].lower()
        markers = ["markdown", "como um", "eu quero", "para que", "critérios de aceitação"]
        assert any(m in text for m in markers), \
            "O prompt não exige formato Markdown nem User Story padrão"

    def test_prompt_has_few_shot_examples(self, prompt):
        """Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot)."""
        text = prompt["system_prompt"]
        assert "exemplo" in text.lower(), "Nenhuma seção de exemplos encontrada"
        assert text.count("Relato:") >= 1, "Exemplos sem entrada (Relato:)"
        assert text.count("Como um") >= 2, "Exemplos sem saída (User Story)"

    def test_prompt_no_todos(self, prompt):
        """Garante que você não esqueceu nenhum `[TODO]` no texto."""
        for field in ("system_prompt", "user_prompt", "description"):
            assert "TODO" not in str(prompt.get(field, "")), \
                f"TODO encontrado no campo '{field}'"

    def test_minimum_techniques(self, prompt):
        """Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas."""
        techniques = prompt.get("techniques_applied", [])
        assert isinstance(techniques, list), "'techniques_applied' deve ser uma lista"
        assert len(techniques) >= 2, f"Mínimo 2 técnicas, encontradas: {len(techniques)}"

    def test_validate_prompt_structure(self, prompt):
        """Valida o prompt com a mesma regra usada pelo push_prompts.py."""
        is_valid, errors = validate_prompt_structure(prompt)
        assert is_valid, f"Erros de estrutura: {errors}"

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])