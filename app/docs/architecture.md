                  Natural-Language Question
                            │
                            ▼
                    ┌──────────────┐
                    │ Agent Planner│
                    └──────┬───────┘
                           │
                    Tool Selection
                           │
          ┌────────────────┼────────────────┐
          ▼                ▼                ▼
     Schema Tool       SQL Tool       Statistics Tool
          │                │                │
          │                ▼                │
          │         ┌──────────────┐        │
          │         │ SQL Validator│        │
          │         └──────┬───────┘        │
          │                │                │
          │        ┌───────┴───────┐        │
          │        ▼               ▼        │
          │      ALLOW            BLOCK     │
          │        │                        │
          └────────┼────────────────────────┘
                   ▼
             Tool Results
                   │
                   ▼
             Agent Synthesis
                   │
                   ▼
       Structured Analytical Response
                   │
                   ▼
            Audit / Trace Log
