import sqlite3


class Database(object):
    def __init__(self, path):
        self.path = path

    def __enter__(self):
        self.connection = sqlite3.connect(self.path)
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.connection.commit()
        else:
            self.connection.rollback()
        self.cursor.close()
        self.connection.close()

# Path: main.py

    def create_database(self):
        with Database('data.db') as db:
            db.execute('CREATE TABLE IF NOT EXISTS users (id INT unique NOT NULL)')
            db.execute('CREATE TABLE IF NOT EXISTS files (vid TEXT, file_id TEXT)')


    def add_file(self, vid, file_id):
        with Database('data.db') as db:
            db.execute('INSERT INTO files VALUES (?, ?)', (vid, file_id))

    def add_user(self, id: int):
        with Database('data.db') as db:
            db.execute('INSERT INTO users VALUES (?)', (id,))

    def get_file(self, vid):
        with Database('data.db') as db:
            db.execute('SELECT file_id FROM files WHERE vid = ?', (vid,))
            return db.fetchone()
