import sqlite3
import os
import levelloader

class Database:
    def __init__(self):
        self.updatelevel = "UPDATE levels SET lastlevel=? WHERE id = 1"
        self.update_high_score = "UPDATE scores SET high_score=? WHERE id=1"
        self.cur = None
        self.con = None
        self.levelunlocked = -1
        self.high_score = 0
        self.leve_loader = levelloader.LevelLoader()

        db_path = "../db"  # Ensure this path is correct relative to your project structure

        if not os.path.isfile(db_path):
            # Database does not exist; create it
            self.con = sqlite3.connect(db_path)
            self.cur = self.con.cursor()
            self.dataexists = False

            # Create 'levels' table
            self.createtable_levels = """
                CREATE TABLE levels(
                    id INTEGER PRIMARY KEY,
                    lastlevel INTEGER
                );
            """
            self.cur.execute(self.createtable_levels)

            # Initialize 'levels' table with first level unlocked
            self.cur.execute("INSERT INTO levels(id, lastlevel) VALUES (?, ?)", (1, 1))
            j = self.cur.execute("select * from levels")

            # Create 'scores' table
            self.createtable_scores = """
                CREATE TABLE scores(
                    id INTEGER PRIMARY KEY,
                    high_score INTEGER
                );
            """
            self.cur.execute(self.createtable_scores)

            # Initialize 'scores' table with a high score of 0
            self.cur.execute("INSERT INTO scores(id, high_score) VALUES (?, ?)", (1, 0))

            self.con.commit()
            self.levelunlocked = 1
            self.high_score = 0
        else:
            # Database exists; connect to it
            self.con = sqlite3.connect(db_path)
            self.cur = self.con.cursor()
            self.dataexists = True
            j = self.cur.execute("select * from levels")
            j = self.cur.fetchall()
            self.levelunlocked = j[0][1]
            # Ensure 'levels' table exists
            try:
                self.cur.execute("SELECT * FROM levels")
                levels = self.cur.fetchall()
                if not levels:
                    # If 'levels' table is empty, initialize it
                    self.cur.execute("INSERT INTO levels(id, lastlevel) VALUES (?, ?)", (1, 1))
                    self.levelunlocked = 1
                else:
                    self.levelunlocked = levels[0][1]
            except sqlite3.OperationalError:
                # 'levels' table does not exist; create it
                self.createtable_levels = """
                    CREATE TABLE levels(
                        id INTEGER PRIMARY KEY,
                        lastlevel INTEGER
                    );
                """
                self.cur.execute(self.createtable_levels)
                self.cur.execute("INSERT INTO levels(id, lastlevel) VALUES (?, ?)", (1, 1))
                self.con.commit()
                self.levelunlocked = 1

            # Ensure 'scores' table exists
            try:
                self.cur.execute("SELECT * FROM scores")
                scores = self.cur.fetchall()
                if not scores:
                    # If 'scores' table is empty, initialize it
                    self.cur.execute("INSERT INTO scores(id, high_score) VALUES (?, ?)", (1, 0))
                    self.high_score = 0
                else:
                    self.high_score = scores[0][1]
            except sqlite3.OperationalError:
                # 'scores' table does not exist; create it
                self.createtable_scores = """
                    CREATE TABLE scores(
                        id INTEGER PRIMARY KEY,
                        high_score INTEGER
                    );
                """
                self.cur.execute(self.createtable_scores)
                self.cur.execute("INSERT INTO scores(id, high_score) VALUES (?, ?)", (1, 0))
                self.con.commit()
                self.high_score = 0

    def get_high_score(self):
        return self.high_score

    def update_high_score_db(self, new_score):
        if new_score > self.high_score:
            self.cur.execute(self.update_high_score, (new_score,))
            self.con.commit()
            self.high_score = new_score

    def insert_level(self):
        # This method seems redundant based on current usage
        self.cur.execute("INSERT INTO levels(id, lastlevel) VALUES (?, ?)", (1, 1))
        self.con.commit()

    def update_level(self):
        self.cur.execute("SELECT lastlevel FROM levels WHERE id = 1")
        k = self.cur.fetchone()[0]
        if k < 5:
            self.cur.execute(self.updatelevel, (k + 1,))
            self.levelunlocked = k + 1
            self.con.commit()

    def get_level(self, i):
        if self.levelunlocked >= i:
            return self.leve_loader.get_Level(i)
        else:
            return "Locked"

if __name__ == '__main__':
    d = Database()
    d.update_level()
