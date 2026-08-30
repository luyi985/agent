
from user.user import User
from db.sqlite_db import SQLiteDB


def test_sqlite_db():
    db = SQLiteDB("./data/data.db")
    user = User(db)
    user.init_db()
    u = user.get_user(1)
    print(u)
    # user_id = user.create_user(
    #     username="Yi",
    #     email="yi@example.com",
    #     password_hash="123",
    #     display_name="YiLu",
    # )
    # print(user_id)


test_sqlite_db()
