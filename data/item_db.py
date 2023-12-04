import sqlite3
from typing import List, Any


class ItemDB:
    def __init__(self):
        self.conn = sqlite3.connect('data_db/santa.db')
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    async def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS item (
                itemid INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                userid INTEGER NOT NULL,
                FOREIGN KEY (userid) REFERENCES user(userid)
            );
        ''')
        self.conn.commit()

    async def add_item(self, userid: int, name: str) -> None:
        self.cursor.execute('''
            INSERT INTO item (name, userid) VALUES (?, ?);
        ''', (name, userid))
        self.conn.commit()

    async def get_items(self, userid: int) -> list[Any]:
        items = self.cursor.execute('''
            SELECT name, itemid FROM item WHERE userid = ?;
        ''', (userid,)).fetchall()
        return items

    async def get_item(self, userid: int, itemid: int) -> str:
        item = self.cursor.execute('''
            SELECT name FROM item WHERE userid = ? AND itemid = ?;
        ''', (userid, itemid)).fetchone()
        return item

    async def delete_item(self, itemid: int) -> None:
        self.cursor.execute('''
            DELETE FROM item WHERE itemid = ?;
        ''', (itemid, ))
        self.conn.commit()

    async def change_item(self, itemid: int, new_name: str) -> None:
        self.cursor.execute('''
            UPDATE item SET name = ? WHERE itemid = ?;
        ''', (new_name, itemid))
        self.conn.commit()
