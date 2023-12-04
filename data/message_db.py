import sqlite3



class MessageDB:
    def __init__(self):
        self.conn = sqlite3.connect('data_db/santa.db')
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    async def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS message (
                messageid INTEGER PRIMARY KEY AUTOINCREMENT,
                userid INTEGER NOT NULL,
                message TEXT NOT NULL,
                date TEXT NOT NULL,
                FOREIGN KEY (userid) REFERENCES user(userid)
            );
        ''')
        self.conn.commit()