import sqlite3
from typing import Any


class SchemaTool:

    def __init__(self, database_path: str):
        self.database_path = database_path

    def inspect(self) -> dict[str, Any]:

        connection = sqlite3.connect(self.database_path)

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT name
                FROM sqlite_master
                WHERE type = 'table'
                  AND name NOT LIKE 'sqlite_%'
                ORDER BY name
                """
            )

            tables = [
                row[0]
                for row in cursor.fetchall()
            ]

            schema = {}

            for table in tables:

                # Table names come from sqlite_master rather
                # than directly from the LLM.
                cursor.execute(
                    f'PRAGMA table_info("{table}")'
                )

                schema[table] = [
                    {
                        "name": row[1],
                        "type": row[2],
                        "nullable": not bool(row[3]),
                        "primary_key": bool(row[5]),
                    }
                    for row in cursor.fetchall()
                ]

            return schema

        finally:
            connection.close()
