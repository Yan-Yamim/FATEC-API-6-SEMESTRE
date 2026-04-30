# Feature: Mapa de Calor + Score de Criticidade

Branch: `marilia/mapa-calor-score-criticidade`  
Data: 2026-04-30

---

## O que foi feito

### 1. Code Review dos arquivos modificados

Antes de qualquer merge, foi feita uma revisão completa dos arquivos em desenvolvimento. Os problemas encontrados e corrigidos foram:

| Arquivo | Problema | Correção |
|---|---|---|
| `pipeline_trigger.py` | `datetime.utcnow()` removido no Python 3.14 | `datetime.now(timezone.utc)` |
| `criticidade.py` | Função `render_mapa_criticidade` morta + `import io` órfão | Removidos |
| `criticidade.py` | `global` sem supressão do linter | `# noqa: PLW0603` |
| `routes/criticidade.py` | Magic numbers `2000`, `2030`, `2` inline | Constantes `_ANO_MIN`, `_ANO_MAX`, `_DIST_MIN_LEN` |
| `routes/criticidade.py` | `logger.info(f"...")` — f-string avaliada mesmo sem log ativo | `logger.info("...", arg1, arg2)` (lazy formatting) |
| `routes/criticidade.py` | Comentários descrevendo o óbvio | Removidos |
| `render_criticidade.py` | `geopandas`, `shapely`, `Patch` importados dentro da função | Movidos para o topo do módulo |
| `render_criticidade.py` | `_output_dir()` chamava `mkdir` a cada render | Substituído por `@lru_cache` |
| `app.py` | Import longo em linha única | Quebrado em multi-linha (isort) |
| `pipeline_trigger.py` | `from datetime import datetime` após `import httpx` | Corrigida ordem stdlib → third-party |
| `tests/test_criticidade.py` | `_AsyncIter` sem type hints | Adicionados |

---

### 2. Atualização das branches

```
upstream/dev  ──►  local dev  ──►  marilia/mapa-calor-score-criticidade
```

- `git fetch upstream` capturou novos commits do repositório original
- `git merge upstream/dev` aplicou no `dev` local (fast-forward)
- `git merge dev` aplicou na feature branch
- **6 conflitos resolvidos** nos arquivos abaixo

---

### 3. Resolução de conflitos e adaptação à refatoração do dev

O merge trouxe uma **refatoração significativa** no `dev`: o padrão de acesso ao MongoDB mudou de um singleton local (`_client`, `_db_name`) para `get_mongo_async_db()` centralizado em `database.py`.

| Arquivo | Conflito | Resolução |
|---|---|---|
| `app.py` | `lifespan` + `close_mongo_client` vs versão sem lifespan | Adotada versão do `dev` — MongoDB gerenciado pelo `database.py` |
| `services/criticidade.py` | Singleton antigo vs novo padrão `get_mongo_async_db` | Adotada versão do `dev` + função `criar_mapa_criticidade` adicionada |
| `services/pipeline_trigger.py` | Funções renomeadas no `dev` | `distribuidora_job_already_triggered` mantida do dev; `get_distribuidora_info` preservada para uso interno |
| `routes/pipeline.py` | Lógica expandida vs `trigger_pipeline_flow` do dev | Adotado `trigger_pipeline_flow` do dev como orquestrador |
| `routes/criticidade.py` | Formatação divergente | Melhorias do code review mantidas |
| `tests/test_criticidade.py` | Nomes de funções mockadas divergentes | Adotada versão do dev (`buscar_dados_realizados`, `buscar_dados_limites`) + testes de `criar_mapa_criticidade` adaptados |

`render_criticidade.py` também foi atualizado: import de `_col` substituído por `get_mongo_collection`.

---

### 4. Alinhamento com o documento de arquitetura

O arquivo `backend/docs/pipeline_trigger_service_di.md` define a regra:

> **Toda lógica de negócio deve entrar no service. O endpoint deve ser um adaptador HTTP fino.**

O fluxo estava errado — as chamadas de criticidade e render estavam na rota. Foram movidas para dentro de `trigger_pipeline_flow`:

**Antes (errado):**
```python
# routes/pipeline.py — lógica de negócio no endpoint ❌
dist_name, _ = await get_distribuidora_info(...)
result = await trigger_pipeline_flow(...)
await calcular_score_criticidade(...)
await criar_mapa_criticidade(...)
await render_tabela_score_criticidade(...)
await render_mapa_calor_criticidade(...)
return result
```

**Depois (correto):**
```python
# routes/pipeline.py — adaptador HTTP fino ✅
return await trigger_pipeline_flow(
    session=session,
    distribuidora_id=request.distribuidora_id,
    ano=request.ano,
)
```

```python
# services/pipeline_trigger.py — orquestrador ✅
async def trigger_pipeline_flow(...) -> dict:
    # 1. pré-condição
    # 2. contexto (distribuidora)
    # 3. download URL + enqueue
    # 4. tracking
    # 5. score de criticidade
    # 6. mapa de criticidade
    # 7. render tabela
    # 8. render mapa de calor
    return resultado
```

---

## Fluxo completo — ponta a ponta

```mermaid
flowchart TD
    Cliente(["🌐 Cliente HTTP\nPOST /pipeline/trigger"])

    subgraph ROTA ["routes/pipeline.py — adaptador HTTP"]
        R1["recebe PipelineTriggerRequest\ninjecta session via Depends"]
        R2{"exceção?"}
        R_409["409 — ValueError"]
        R_404["404 — LookupError"]
        R_502["502 — RuntimeError"]
        R_202["202 — PipelineTriggerResponse"]
    end

    subgraph SERVICE ["services/pipeline_trigger.py — orquestrador"]
        S1["distribuidora_job_already_triggered\nPostgreSQL — verifica job existente"]
        S2{"já disparada?"}
        S_val["raise ValueError"]
        S3["_get_distribuidora_info\nPostgreSQL — busca dist_name e job_id atual"]
        S4{"não encontrada?"}
        S_look["raise LookupError"]
        S5["resolve_download_url_from_aneel\nArcGIS API — valida item GDB"]
        S6["enqueue_download_gdb\nCelery — gera job_id e enfileira task"]
        S7["save_distribuidora_job_tracking\nPostgreSQL — persiste job_id + timestamp"]
        S8["calcular_score_criticidade\nMongoDB — DEC/FEC realizados e limites"]
        S9["criar_mapa_criticidade\nMongoDB — scores por conjunto com categoria"]
        S10["render_tabela_score_criticidade\nMatplotlib — tabela PNG em /output/images"]
        S11["render_mapa_calor_criticidade\nGeoPandas + Matplotlib — mapa PNG"]
        S12["retorna dict com job_id, task_id, status, url"]
    end

    subgraph MONGO ["MongoDB"]
        M1[("dec_fec_realizado")]
        M2[("dec_fec_limite")]
        M3[("score_criticidade")]
        M4[("mapa_criticidade")]
        M5[("segmentos_mt_geo")]
    end

    subgraph PG ["PostgreSQL"]
        P1[("Distribuidora")]
    end

    subgraph CELERY ["Celery Worker"]
        C1["task_download_gdb\nbaixa arquivo GDB da ANEEL"]
        C2["task_extrair_gdb\nextrai e carrega geometrias"]
    end

    subgraph OUTPUT ["Sistema de arquivos"]
        O1["tabela_score_DIST_ANO.png"]
        O2["mapa_calor_DIST_ANO.png"]
    end

    Cliente --> R1
    R1 --> S1
    S1 --> P1
    S1 --> S2
    S2 -->|"sim"| S_val --> R2
    S2 -->|"não"| S3
    S3 --> P1
    S3 --> S4
    S4 -->|"sim"| S_look --> R2
    S4 -->|"não"| S5
    S5 -->|"LookupError / RuntimeError"| R2
    S5 --> S6
    S6 --> C1
    C1 --> C2
    C2 --> M5
    S6 --> S7
    S7 --> P1
    S7 --> S8
    S8 --> M1
    S8 --> M2
    S8 --> M3
    S8 --> S9
    S9 --> M1
    S9 --> M2
    S9 --> M4
    S9 --> S10
    S10 --> M3
    S10 --> O1
    S10 --> S11
    S11 --> M3
    S11 --> M4
    S11 --> M5
    S11 --> O2
    S11 --> S12
    S12 --> R2
    R2 -->|"ValueError"| R_409
    R2 -->|"LookupError"| R_404
    R2 -->|"RuntimeError"| R_502
    R2 -->|"ok"| R_202
    R_202 --> Cliente

    style ROTA fill:#1a3a5c,color:#fff
    style SERVICE fill:#1a4a2e,color:#fff
    style MONGO fill:#4a2a1a,color:#fff
    style PG fill:#2a2a4a,color:#fff
    style CELERY fill:#4a1a3a,color:#fff
    style OUTPUT fill:#3a3a1a,color:#fff
```

---

## Estrutura de arquivos envolvidos

```
backend/
├── routes/
│   ├── criticidade.py        # GET /etl/criticidade — endpoint de consulta
│   └── pipeline.py           # POST /pipeline/trigger — adaptador HTTP fino
├── services/
│   ├── criticidade.py        # calcular_score_criticidade, criar_mapa_criticidade
│   ├── pipeline_trigger.py   # trigger_pipeline_flow — orquestrador principal
│   └── render_criticidade.py # render_tabela_score, render_mapa_calor
├── tests/
│   └── test_criticidade.py   # testes unitários do fluxo de criticidade
└── docs/
    ├── pipeline_trigger_service_di.md  # regras de arquitetura do /trigger
    └── sessao_mapa_calor_score.md      # este documento
```
