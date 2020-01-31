import sqlite3 as sq

class Sqlm():

    def __init__(self, basename, src, dest):
        self.database = sq.connect(basename)
        self.open_base(src, dest)

    def open_base(self, src, dest):
        # src - language which we translate to, dest - lang. we translate from
        self.tabname = src + dest
        self.control = self.database.cursor()
        self.control.execute("""CREATE TABLE IF NOT EXISTS {tabname} ({src} text, {dest} text)""".format(
            tabname = self.tabname, src = src, dest = dest))

        print("{src}-{dest} was successfully opened".format(src = src, dest = dest))


    def add_word(self, src_w, dest_w):
        # src_w - word which should be translated and presented as a dest_w
        self.control.execute("""INSERT INTO {tabname} VALUES ('{src_w}', '{dest_w}')""".format(
                tabname = self.tabname, src_w = src_w, dest_w = dest_w))
        self.database.commit()

    def select(self, sattributes: dict):
        sqlm_request = "SELECT * FROM {tabname} WHERE ".format(tabname=self.tabname)

        for on, attribute in enumerate(sattributes.keys()):
            sqlm_request += "{attribute} = '{value}'".format(
                attribute=attribute, value=sattributes.get(attribute))
            if not (len(sattributes.keys()) - on == 1):
                sqlm_request += " AND "

        self.control.execute(sqlm_request)
        return self.control.fetchone()

    def delete(self, attribute, value):
        self.control.execute("""DELETE FROM {tabname} WHERE {attribute} = {value}""".format(
            tabname = self.tabname, attribute = attribute, value = value))

    def close(self):
        self.database.close()

    def is_filled(self):
        self.control.execute("SELECT * FROM {tabname}".format(tabname=self.tabname))
        items = self.control.fetchall()

        if len(items) == 0:
            return False
        return items
