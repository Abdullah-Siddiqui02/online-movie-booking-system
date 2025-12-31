import sqlite3

class Database:
    def __init__(self, db_file="movies.db"):
        self.conn = sqlite3.connect(db_file)
        self.cur = self.conn.cursor()
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                director TEXT NOT NULL,
                year INTEGER,
                rating INTEGER
            )
        """)
        self.conn.commit()

    def add_movie(self, title: str, director: str, year: int, rating: int):
        self.cur.execute("INSERT INTO movies VALUES (NULL, ?, ?, ?, ?)", 
                         (title, director, year, rating))
        self.conn.commit()

    def fetch_all(self):
        self.cur.execute("SELECT * FROM movies")
        return self.cur.fetchall()

    def remove_movie(self, id: int):
        self.cur.execute("DELETE FROM movies WHERE id=?", (id,))
        self.conn.commit()

    def update_movie(self, id: int, title: str, director: str, year: int, rating: int):
        self.cur.execute("""
            UPDATE movies SET title=?, director=?, year=?, rating=? WHERE id=?
        """, (title, director, year, rating, id))
        self.conn.commit()

    def __del__(self):
        self.conn.close()