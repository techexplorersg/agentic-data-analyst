from dataclasses import dataclass


@dataclass(frozen=True)
class PlanStep:
    name: str
    description: str


class AnalyticsPlanner:

    def create_plan(
        self,
        question: str,
    ) -> list[PlanStep]:

        if not question.strip():
            raise ValueError(
                "Question cannot be empty"
            )

        return [
            PlanStep(
                name="inspect_schema",
                description=(
                    "Inspect available tables "
                    "and columns."
                ),
            ),
            PlanStep(
                name="generate_sql",
                description=(
                    "Generate a read-only analytical "
                    "query from the question and schema."
                ),
            ),
            PlanStep(
                name="validate_sql",
                description=(
                    "Validate SQL against application "
                    "security policies."
                ),
            ),
            PlanStep(
                name="execute_sql",
                description=(
                    "Execute the approved query using "
                    "read-only database access."
                ),
            ),
            PlanStep(
                name="synthesize",
                description=(
                    "Transform tool results into a "
                    "structured analytical response."
                ),
            ),
        ]
