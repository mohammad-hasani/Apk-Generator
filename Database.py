import pypyodbc


class Database(object):
    def __init__(self):
        pass

    def connect(self):
        self.con = pypyodbc.connect(driver='{SQL Server}', server='185.55.226.129', database='QR', uid='sa', pwd='D4c3b2a1')

    def select(self, query):
        cur = self.con.cursor()
        cur.execute(query)
        data = cur.fetchall()
        cur.close()
        return data

    def update_or_insert(self, query):
        cur = self.con.cursor()
        try:
            cur.execute(query)
            self.con.commit()
            return True
        except:
            return False

    def close(self):
        self.con.close()
