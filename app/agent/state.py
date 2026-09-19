from dataclasses import dataclass, field
from typing import Any


@dataclass
class AgentState:
    request_id: str
    question: str

    schema: dict[str, Any] | None = None
    generated_sql: str | None = None
    sql_result: list[dict[str, Any]] | None = None

    steps: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
