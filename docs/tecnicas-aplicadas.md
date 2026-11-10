# Técnicas Aplicadas (Fase 2)

**Contexto:** o prompt recebe um relato de bug e deve gerar uma User Story. O dataset tem bugs simples, médios e complexos, e a resposta esperada fica maior conforme a complexidade. As técnicas foram escolhidas para o modelo usar o formato certo em cada nível e cobrir o conteúdo esperado sem inventar fatos.

Prompt: [`prompts/bug_to_user_story_v2.yml`](../prompts/bug_to_user_story_v2.yml)

| Técnica | Por que | Como foi aplicada |
|---|---|---|
| **Few-shot Learning** | Mostrar o formato funciona melhor do que só descrevê-lo. | 3 exemplos completos, um por nível (botão no Firefox, PDF de nota fiscal, agendamento de clínica). São bugs que não estão no dataset, para não medir memorização. |
| **Role Prompting** | Define o vocabulário de produto e permite detalhe técnico quando necessário. | "Você é um Product Manager sênior, com base técnica...", mais a regra de usar uma persona específica (ex.: "cliente usando Safari"). |
| **Skeleton of Thought** | Cada nível tem uma estrutura de resposta diferente. | Seção `# FORMATO` com um esqueleto para SIMPLES (história + critérios), MÉDIO (+ seções técnicas e contexto) e COMPLEXO (seções `===`, tasks em fases, métricas de sucesso). |
| **Chain of Thought** | Analisar e classificar o relato antes de escrever evita formato errado e fatos esquecidos. | `# PASSO A PASSO` com 5 etapas internas: extrair fatos, definir persona, classificar, consultar o checklist e conferir a cobertura. O raciocínio não aparece na resposta. |

**Complemento: checklist por tipo de bug.** Lista o que o gabarito costuma esperar para cada tipo de problema. Exemplos: em bugs de lentidão, meta de tempo (< 2 s); em webhooks, status "pendente" → "aprovado", e-mail e log de auditoria; em falhas de segurança, HTTP 403 e OWASP. O checklist foi criado a partir dos comentários dos juízes na 1ª iteração (ver [resultados](resultados-finais.md#iterações)).
