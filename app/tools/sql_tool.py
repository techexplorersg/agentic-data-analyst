import sqlite3
from typing import Any

from app.security.sql_validator import SQLValidator


class SQLExecutionError(Exception):
    pass


class SQLTool:

    def __init__(
        self,
        database_path: str,
        validator: SQLValidator,
        max_rows: int = 100,
    ):
        self.database_path = database_path
        self.validator = validator
        self.max_rows = max_rows

    def execute(
        self,
        sql: str,
    ) -> list[dict[str, Any]]:

        validation = self.validator.validate(sql)

        if not validation.allowed:
            raise SQLExecutionError(
                validation.reason
                or "Query rejected by SQL policy"
            )

        # SQLite URI mode lets the application open
        # the database itself as read-only.
        uri = f"file:{self.database_path}?mode=ro"

        connection = sqlite3.connect(
            uri,
            uri=True,
        )

        connection.row_factory = sqlite3.Row

        try:
            cursor = connection.execute(sql)

            rows = cursor.fetchmany(
                self.max_rows + 1
            )

            if len(rows) > self.max_rows:
                raise SQLExecutionError(
                    f"Query exceeded maximum result size "
                    f"of {self.max_rows} rows"
                )

            return [
                dict(row)
                for row in rows
            ]

        except sqlite3.Error as exc:
            raise SQLExecutionError(
                f"Database execution failed: {exc}"
            ) from exc

        finally:
            connection.close()
