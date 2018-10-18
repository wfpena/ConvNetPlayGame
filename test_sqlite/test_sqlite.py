import sqlite3
import os

class SequenceImg():

    def __init__(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(BASE_DIR, "tensor_db.db")
        print('Base dir:', BASE_DIR)

    def set_current(self, v, clean_index=True):
        with sqlite3.connect(self.db_path) as db:
            cur = db.cursor()
            if clean_index:
                cur.execute('delete from img_index')
            cur.execute('insert into img_index (current) values ({0})'.format(v))

            db.commit()
            #db.close()

    def get_current(self):
        with sqlite3.connect(self.db_path) as db:
            cur = db.cursor()
            cur.execute("SELECT current FROM img_index limit 1")
            num = cur.fetchone()
            return num[0]

    def increment_sq(self):
        with sqlite3.connect(self.db_path) as db:
            cur = db.cursor()
            cur.execute("SELECT current FROM img_index limit 1")
            num = cur.fetchone()
            cur.execute('delete from img_index')
            cur.execute('insert into img_index (current) values ({0})'.format(num[0] + 1))
            db.commit()
            self.query_value()

    def decrement_sq(self):
        with sqlite3.connect(self.db_path) as db:
            cur = db.cursor()
            cur.execute("SELECT current FROM img_index limit 1")
            num = cur.fetchone()
            cur.execute('delete from img_index')
            cur.execute('insert into img_index (current) values ({0})'.format(num[0] - 1))
            db.commit()
            self.query_value()

    def query_value(self):
        with sqlite3.connect(self.db_path) as db:
            cur = db.cursor()
            cur.execute("SELECT * FROM img_index")

            rows = cur.fetchall()

            for row in rows:
                print(row)

    def zero_index(self):
        with sqlite3.connect(self.db_path) as db:
            cur = db.cursor()
            cur.execute('delete from img_index')
            cur.execute('insert into img_index (current) values (0)')
            db.commit()
            self.query_value()

sq = SequenceImg()
#sq.increment_sq()
sq.set_current(342)
print(sq.get_current())