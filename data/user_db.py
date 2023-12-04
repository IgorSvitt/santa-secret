import sqlite3


class UserDB:
    def __init__(self):
        self.conn = sqlite3.connect('data_db/santa.db')
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    async def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS user (
                userid INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                username TEXT NOT NULL UNIQUE,
                about TEXT,
                room TEXT NOT NULL,
                link_to_vk TEXT NOT NULL,
                count_messages INTEGER NOT NULL,
                santa_to_id INTEGER
            );
        ''')
        self.conn.commit()

    async def add_user(self, userid: int, name: str, username: str, room: str, link_to_vk: str, count_messages: int):
        self.cursor.execute('''
            INSERT INTO user (userid, name, username, room, link_to_vk, count_messages)
            VALUES (?, ?, ?, ?, ?, ?);
        ''', (userid, name, username, room, link_to_vk, count_messages))
        self.conn.commit()

    async def get_user(self, userid: int):
        self.cursor.execute('''
            SELECT * FROM user WHERE userid = ?;
        ''', (userid,))
        return self.cursor.fetchone()

    async def change_name(self, userid: int, name: str):
        self.cursor.execute('''
            UPDATE user SET name = ? WHERE userid = ?;
        ''', (name, userid))
        self.conn.commit()

    async def change_room(self, userid: int, room: str):
        self.cursor.execute('''
            UPDATE user SET room = ? WHERE userid = ?;
        ''', (room, userid))
        self.conn.commit()

    async def change_link_to_vk(self, userid: int, link_to_vk: str):
        self.cursor.execute('''
            UPDATE user SET link_to_vk = ? WHERE userid = ?;
        ''', (link_to_vk, userid))
        self.conn.commit()

    async def get_users(self):
        self.cursor.execute('''
            SELECT * FROM user;
        ''')
        return self.cursor.fetchall()

    async def get_users_username(self):
        self.cursor.execute('''
            SELECT username FROM user;
        ''')
        return self.cursor.fetchall()

    async def change_santa(self, userid: int, santa_to_id: int):
        self.cursor.execute('''
            UPDATE user SET santa_to_id = ? WHERE userid = ?;
        ''', (santa_to_id, userid))
        self.conn.commit()

    async def get_santa(self, santa_to_id: int):
        self.cursor.execute('''
            SELECT * FROM user WHERE userid = ?;
        ''', (santa_to_id,))
        return self.cursor.fetchone()

    async def change_about(self, userid: int, about: str):
        self.cursor.execute('''
            UPDATE user SET about = ? WHERE userid = ?;
        ''', (about, userid))
        self.conn.commit()