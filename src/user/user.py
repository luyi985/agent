from collections.abc import Mapping

from db.sqlite_db import SQLiteDB


class User:
    def __init__(self, db: SQLiteDB):
        self.db = db

    def init_db(self) -> None:
        with self.db as db:
            db.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    email TEXT NOT NULL UNIQUE,
                    password_hash TEXT NOT NULL,
                    display_name TEXT,
                    is_active INTEGER NOT NULL DEFAULT 1,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

    def create_user(
        self,
        username: str,
        email: str,
        password_hash: str,
        display_name: str | None = None,
    ) -> int:
        with self.db as db:
            user_id = db.execute(
                """
                INSERT INTO users (username, email, password_hash, display_name)
                VALUES (?, ?, ?, ?)
                """,
                (username, email, password_hash, display_name),
            )

        if user_id is None:
            raise RuntimeError("INSERT did not return a user ID")

        return user_id

    def get_user(self, user_id: int) -> Mapping[str, object] | None:
        with self.db as db:
            return db.fetch_one(
                """
                SELECT * FROM users WHERE id = ?
                """,
                (user_id,),
            )
