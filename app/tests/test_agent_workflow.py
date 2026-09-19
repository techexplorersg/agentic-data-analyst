from app.agent.llm import MockLLMProvider
from app.agent.orchestrator import AnalyticsAgent
from app.agent.planner import AnalyticsPlanner
from app.security.sql_validator import SQLValidator
from app.tools.schema_tool import SchemaTool
from app.tools.sql_tool import SQLTool


def test_agent_executes_governed_analysis():

    database = "data/sample.db"

    validator = SQLValidator()

    agent = AnalyticsAgent(
        schema_tool=SchemaTool(database),
        sql_tool=SQLTool(
            database,
            validator,
        ),
        sql_validator=validator,
        llm=MockLLMProvider(),
        planner=AnalyticsPlanner(),
    )

    result = agent.run(
        "Show total revenue by region"
    )

    assert result["request_id"]

    assert (
        "SELECT"
        in result["sql"].upper()
    )

    assert len(
        result["result"]
    ) > 0

    assert (
        "sql_validated"
        in result["steps"]
    )

    assert (
        "sql_executed"
        in result["steps"]
    )
