from abc import ABC, abstractmethod


class LLMProvider(ABC):

    @abstractmethod
    def generate_sql(
        self,
        question: str,
        schema: dict,
    ) -> str:
        raise NotImplementedError


class MockLLMProvider(LLMProvider):
    """
    Deterministic provider for tests and local demos.

    Production/provider integrations can implement the
    same interface without coupling orchestration code
    to one LLM vendor.
    """

    def generate_sql(
        self,
        question: str,
        schema: dict,
    ) -> str:

        question_lower = question.lower()

        if (
            "revenue" in question_lower
            and "region" in question_lower
        ):
            return """
                SELECT
                    region,
                    SUM(revenue) AS total_revenue
                FROM sales
                GROUP BY region
                ORDER BY total_revenue DESC
                LIMIT 10
            """

        raise ValueError(
            "Mock provider does not support this question."
        )
