# Architecture

## Overview

```
task entra (/tos "cria um botão de submit")
        ↓
[orchestrator]
  1. classifica a tarefa (tipo, complexidade)
  2. checa registry: agente adequado já existe?
  3. se não → monta config do catalog → salva no registry
  4. gera ExecutionPlan JSON
        ↓
[brainstorm]  ← roda para medium/high complexity
  analisa requisitos explícitos, implícitos, ambiguidades
        ↓
[agentes em paralelo ou sequencial]
  backend-developer → pr-creator → pr-reviewer
        ↓
[synthesizer]
  agrega outputs via context.json → resultado final
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
└── index.md    ← lista de agentes salvos + quando usar
```

---

## Classificação de tarefas

Antes de spawnar, o orquestrador classifica:

| Campo | Exemplo |
|-------|---------|
| tipo | frontend / backend / fullstack / infra / fix / other |
| complexidade | low / medium / high |
| precisa de git | sim / não |
| agentes sugeridos | backend-developer, pr-creator, pr-reviewer |
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

## Monorepo mode

Quando `/tos` roda dentro deste repo, o código gerado vai para `projects/{nome}/` em vez do diretório atual:

| Condição | Modo | Código vai para |
|----------|------|-----------------|
| `.claude/agents/orchestrator.md` existe no cwd | Monorepo | `projects/{project-name}/` |
| Caso contrário | Externo | Diretório atual |

---

## Estrutura de pastas completa

```
claude-dynamic-agents/
├── CLAUDE.md
├── README.md
├── projects/                     ← projetos gerados (monorepo mode)
│   └── {project-name}/
├── .claude/
│   ├── settings.json
│   ├── catalog/
│   │   ├── skills.md
│   │   ├── mcps.md
│   │   └── models.md
│   ├── registry/
│   │   └── index.md              ← inicialmente vazio, cresce com o uso
│   ├── agents/
│   │   ├── brainstorm.md         ← pré-análise (medium/high complexity)
│   │   ├── orchestrator.md       ← THE BRAIN
│   │   └── synthesizer.md
│   ├── skills/                   ← 15 skills instaladas
│   │   ├── execution-plan/
│   │   ├── fastapi-patterns/
│   │   ├── react-patterns/
│   │   ├── postgres-patterns/
│   │   ├── security-patterns/
│   │   ├── frontend-design/
│   │   ├── search-first/
│   │   ├── agentic-engineering/
│   │   ├── api-design/
│   │   ├── deployment-patterns/
│   │   ├── verification-loop/
│   │   ├── using-git-worktrees/
│   │   ├── dispatching-parallel-agents/
│   │   ├── subagent-driven-development/
│   │   └── workflow-orchestration-patterns/
│   ├── rules/
│   │   ├── orchestration.md
│   │   ├── agent-contracts.md
│   │   └── failure-handling.md
│   └── commands/
│       ├── tos.md                ← /tos [task] — entry point principal
│       └── plan.md               ← /plan (dry-run)
├── workspace/
│   └── {run-id}/                 ← outputs efêmeros de cada run
│       ├── context.json          ← estado compartilhado entre agentes
│       └── activity.jsonl        ← log de eventos append-only
├── examples/
│   ├── todo-app/
│   └── blog-platform/
└── docs/
    ├── architecture.md           ← este arquivo
    ├── catalog.md
    ├── agent-lifecycle.md
    ├── context-propagation.md
    ├── failure-handling.md
    ├── observability.md
    └── pr-review-flow.md
```
