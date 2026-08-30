import sqlite3
from collections.abc import Mapping
from typing import cast

from db.abs_db import AbstractDB, Parameters


class SQLiteDB(AbstractDB):
    def __init__(self, database_path: str):
        self.database_path: str = database_path
        self.connection: sqlite3.Connection | None = None

    def connect(self) -> None:
        self.connection = sqlite3.connect(self.database_path)
        self.connection.row_factory = sqlite3.Row

    def execute(
        self,
        query: str,
        parameters: Parameters = None,
    ) -> int | None:
        if self.connection is None:
            raise RuntimeError("Database is not connected")

        cursor = self.connection.execute(
            query,
            parameters if parameters is not None else (),
        )
        self.connection.commit()
        row_id = cursor.lastrowid
        cursor.close()
        return row_id

    def fetch_one(
        self,
        query: str,
        parameters: Parameters = None,
    ) -> Mapping[str, object] | None:
        if self.connection is None:
            raise RuntimeError("Database is not connected")

        row = self.connection.execute(
            query,
            parameters if parameters is not None else (),
        ).fetchone()

        if row is None:
            return None

        return cast(dict[str, object], dict(row))

    def fetch_all(
        self,
        query: str,
        parameters: Parameters = None,
    ) -> list[Mapping[str, object]]:
        if self.connection is None:
            raise RuntimeError("Database is not connected")

        rows = self.connection.execute(
            query,
            parameters if parameters is not None else (),
        ).fetchall()

        return [cast(dict[str, object], dict(row)) for row in rows]

    def close(self) -> None:
        if self.connection is not None:
            self.connection.close()
            self.connection = None
