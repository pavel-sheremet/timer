import sqlite3
from sqlite3 import Error


class DB:
    db_file = None

    def __init__(self):
        self.db_file = 'timer.db'
        self.create_connection()

    def insert(self, start, end):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("insert into loops(start_date_time, end_date_time) values (?, ?)", (start, end))
        conn.commit()
        conn.close()

    def select(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("select * from loops order by id desc")
        res = cursor.fetchall()
        conn.close()

        return res

    def create_connection(self):
        try:
            conn = sqlite3.connect(self.db_file)
            conn.execute('''CREATE TABLE loops (
                id INTEGER PRIMARY KEY,
                start_date_time timestamp,
                end_date_time timestamp
            )''')
            conn.close()
        except Error as e:
            print(e)
        finally:
            if conn:
                conn.close()
