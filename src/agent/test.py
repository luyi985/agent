from db.sqlite_db import SQLiteDB


def test_sqlite_db():
    db = SQLiteDB("./data.db")
    with db as conn:
        conn.execute(
            "CREATE TABLE users (id INTEGER, name TEXT)"
        )

        conn.execute(
            "INSERT INTO users VALUES (?, ?)",
            (1, "Alice"),
        )

        user = conn.fetch_one(
            "SELECT * FROM users WHERE id = ?",
            (1,),
        )
        print(user)

test_sqlite_db()
