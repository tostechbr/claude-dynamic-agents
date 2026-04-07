# Architecture

## Overview

```
task entra (/orchestrate "cria um botão de submit")
        ↓
[orchestrator]
  1. classifica a tarefa (tipo, complexidade)
  2. checa registry: agente adequado já existe?
  3. se não → monta config do catalog → salva no registry
  4. gera ExecutionPlan JSON
        ↓
[agentes em paralelo ou sequencial]
  react-developer → pr-creator → pr-reviewer
        ↓
[synthesizer]
  agrega outputs → resultado final
```

---

## Duas camadas distintas

### Catalog (estático, curado manualmente)
Paleta de ingredientes disponíveis. Não muda com o uso.

```
.claude/catalog/
├── skills.md    ← conhecimento de domínio (como pensar)
├── mcps.md      ← ferramentas externas (o que pode fazer)
└── models.md    ← regras de seleção de modelo
```

### Registry (dinâmico, cresce com o uso)
Agentes já montados e salvos de runs anteriores. O orquestrador consulta aqui antes de criar do zero.

```
.claude/registry/
├── index.md                  ← lista de agentes salvos + quando usar
├── react-developer.json      ← config salva de um run anterior
└── backend-developer.json
```

---

## Classificação de tarefas

Antes de spawnar, o orquestrador classifica:

| Campo | Exemplo |
|-------|---------|
| tipo | frontend / backend / fullstack / infra |
| complexidade | low / medium / high |
| precisa de git | sim / não |
| agentes sugeridos | react-developer, pr-creator, pr-reviewer |
| execução | sequential / parallel / mixed |

Isso evita over-engineering: um botão não precisa de 5 agentes.

---

## Execução paralela vs sequencial

```json
{
  "agents": [
    { "role": "db-architect",       "depends_on": null },
    { "role": "backend-developer",  "depends_on": "db-architect" },
    { "role": "frontend-developer", "depends_on": "db-architect" },
    { "role": "pr-creator",         "depends_on": ["backend-developer", "frontend-developer"] },
    { "role": "pr-reviewer",        "depends_on": "pr-creator" }
  ]
}
```

- `depends_on: null` → pode rodar imediatamente
- `depends_on: ["A", "B"]` → espera ambos terminarem (barrier)
- Agentes sem dependência entre si rodam em paralelo

---

## Estrutura de pastas completa

```
claude-dynamic-agents/
├── CLAUDE.md
├── README.md
├── .claude/
│   ├── settings.json
│   ├── catalog/
│   │   ├── skills.md
│   │   ├── mcps.md
│   │   └── models.md
│   ├── registry/
│   │   └── index.md          ← inicialmente vazio, cresce com o uso
│   ├── agents/
│   │   ├── orchestrator.md
│   │   └── synthesizer.md
│   ├── skills/
│   │   ├── execution-plan/
│   │   ├── fastapi-patterns/
│   │   ├── react-patterns/
│   │   └── postgres-patterns/
│   ├── rules/
│   │   ├── orchestration.md
│   │   ├── agent-contracts.md
│   │   └── failure-handling.md
│   └── commands/
│       ├── orchestrate.md
│       └── plan.md
├── workspace/
│   └── {run-id}/             ← outputs efêmeros de cada run
├── examples/
│   ├── todo-app/
│   └── blog-platform/
└── docs/
    ├── architecture.md       ← este arquivo
    ├── catalog.md
    ├── agent-lifecycle.md
    ├── context-propagation.md
    ├── failure-handling.md
    └── pr-review-flow.md
```
