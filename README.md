# Agentic-Data-Analyst
Governed agentic analytics reference implementation for natural-language data exploration with safe SQL generation, tool execution, validation, auditability, and structured insights.

```text
                     USER
                      │
                      ▼
             Natural Language Query
                      │
                      ▼
              ┌──────────────┐
              │    Planner   │
              └──────┬───────┘
                     │
                     ▼
              Schema Discovery
                     │
                     ▼
               LLM Provider
                     │
                     ▼
               Proposed SQL
                     │
                     ▼
             ┌───────────────┐
             │ Policy Engine │
             └───────┬───────┘
                     │
                ALLOW / BLOCK
                     │
                     ▼
            Read-Only Database
                     │
                     ▼
               Result Limit
                     │
                     ▼
              Agent Synthesis
                     │
                     ▼
           Structured Response
                     │
                     ▼
                Audit Trail
```

The language model proposes actions; it does not own authorization. SQL passes through deterministic application policy before execution, and the database is opened with read-only access. This creates separate reasoning, authorization, and execution boundaries.
