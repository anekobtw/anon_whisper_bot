import sqlite3


class DBManager:
    def __init__(self, db_name: str, table_schema: str) -> None:
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

        self.cursor.execute(table_schema)
        self.connection.commit()

    def execute_query(self, query: str, params: tuple = ()) -> None:
        self.cursor.execute(query, params)
        self.connection.commit()

    def fetch_all(self, query: str, params: tuple = ()) -> list:
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def fetch_one(self, query: str, params: tuple = ()) -> list:
        self.cursor.execute(query, params)
        return self.cursor.fetchone()


class UsersManager(DBManager):
    def __init__(self):
        table_schema = """CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER,
            sent INTEGER,
            received INTEGER,
            is_banned BOOLEAN
        )"""
        super().__init__("databases/users.db", table_schema)

    def create_user(self, user_id: int) -> None:
        if not self.user_exists(user_id):
            self.execute_query(
                "INSERT INTO users(user_id, sent, received, is_banned) VALUES (?, ?, ?, ?)",
                (user_id, 0, 0, False),
            )

    def ban_user(self, user_id: int) -> None:
        self.execute_query("UPDATE users SET is_banned = True WHERE user_id = ?", (user_id,))

    def unban_user(self, user_id: int) -> None:
        self.execute_query("UPDATE users SET is_banned = False WHERE user_id = ?", (user_id,))

    def is_banned(self, user_id: int) -> bool:
        return self.get_user(user_id)[3]

    def user_exists(self, user_id: int) -> bool:
        if self.get_user(user_id):
            return True
        return False

    def get_user(self, user_id: int) -> list:
        return self.fetch_one("SELECT * FROM users WHERE user_id = ? LIMIT 1", (user_id,))

    def user_sent_message(self, user_id: int) -> None:
        self.execute_query("UPDATE users SET sent = sent + 1 WHERE user_id = ?", (user_id,))

    def user_received_message(self, user_id: int) -> None:
        self.execute_query("UPDATE users SET received = received + 1 WHERE user_id = ?", (user_id,))


class MessagesManager(DBManager):
    def __init__(self):
        table_schema = """CREATE TABLE IF NOT EXISTS messages (
            message_id INTEGER
        )"""
        super().__init__("databases/messages.db", table_schema)

    def insert_message(self, message_id: int) -> None:
        self.execute_query("INSERT INTO messages (message_id) VALUES (?)", (message_id,))

    def is_in_db(self, message_id: int) -> bool:
        if self.fetch_one("SELECT * FROM messages WHERE message_id = ? LIMIT 1", (message_id,)):
            return True
        return False
