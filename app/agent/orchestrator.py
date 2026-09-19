import uuid
from dataclasses import asdict
from typing import Any

from app.agent.llm import LLMProvider
from app.agent.planner import AnalyticsPlanner
from app.agent.state import AgentState
from app.security.sql_validator import SQLValidator
from app.tools.schema_tool import SchemaTool
from app.tools.sql_tool import SQLTool


class AnalyticsAgent:

    def __init__(
        self,
        schema_tool: SchemaTool,
        sql_tool: SQLTool,
        sql_validator: SQLValidator,
        llm: LLMProvider,
        planner: AnalyticsPlanner,
    ):
        self.schema_tool = schema_tool
        self.sql_tool = sql_tool
        self.sql_validator = sql_validator
        self.llm = llm
        self.planner = planner

    def run(
        self,
        question: str,
    ) -> dict[str, Any]:

        state = AgentState(
            request_id=str(uuid.uuid4()),
            question=question,
        )

        plan = self.planner.create_plan(
            question
        )

        state.steps.append(
            "plan_created"
        )

        try:
            state.schema = (
                self.schema_tool.inspect()
            )

            state.steps.append(
                "schema_inspected"
            )

            state.generated_sql = (
                self.llm.generate_sql(
                    question=question,
                    schema=state.schema,
                )
            )

            state.steps.append(
                "sql_generated"
            )

            validation = (
                self.sql_validator.validate(
                    state.generated_sql
                )
            )

            if not validation.allowed:
                raise ValueError(
                    validation.reason
                )

            state.steps.append(
                "sql_validated"
            )

            state.sql_result = (
                self.sql_tool.execute(
                    state.generated_sql
                )
            )

            state.steps.append(
                "sql_executed"
            )

            response = self._synthesize(
                state
            )

            state.steps.append(
                "response_synthesized"
            )

            return {
                "request_id": state.request_id,
                "question": question,
                "plan": [
                    asdict(step)
                    for step in plan
                ],
                "sql": state.generated_sql,
                "result": state.sql_result,
                "analysis": response,
                "steps": state.steps,
            }

        except Exception as exc:

            state.errors.append(str(exc))

            raise

    @staticmethod
    def _synthesize(
        state: AgentState,
    ) -> dict[str, Any]:

        rows = state.sql_result or []

        return {
            "row_count": len(rows),
            "message": (
                f"Analysis completed using "
                f"{len(rows)} returned rows."
            ),
        }
