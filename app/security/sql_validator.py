import re
from dataclasses import dataclass


@dataclass(frozen=True)
class ValidationResult:
    allowed: bool
    reason: str | None = None


class SQLValidator:
    """
    Conservative SQL policy for an analytical agent.

    The agent receives read-only access by policy rather than being trusted
    simply because the LLM was instructed not to modify data.
    """

    BLOCKED_KEYWORDS = {
        "INSERT",
        "UPDATE",
        "DELETE",
        "DROP",
        "ALTER",
        "TRUNCATE",
        "CREATE",
        "REPLACE",
        "GRANT",
        "REVOKE",
        "ATTACH",
        "DETACH",
        "PRAGMA",
    }

    def validate(self, sql: str) -> ValidationResult:
        normalized = re.sub(r"\s+", " ", sql).strip()

        if not normalized:
            return ValidationResult(False, "Empty SQL statement")

        # Keep the reference implementation deliberately conservative.
        if ";" in normalized.rstrip(";"):
            return ValidationResult(
                False,
                "Multiple SQL statements are not permitted",
            )

        tokens = {
            token.upper()
            for token in re.findall(r"\b[A-Za-z_]+\b", normalized)
        }

        blocked = sorted(tokens & self.BLOCKED_KEYWORDS)

        if blocked:
            return ValidationResult(
                False,
                f"Blocked SQL operation: {', '.join(blocked)}",
            )

        first_token = normalized.split(maxsplit=1)[0].upper()

        if first_token not in {"SELECT", "WITH"}:
            return ValidationResult(
                False,
                "Only SELECT or WITH queries are permitted",
            )

        return ValidationResult(True)
