
import uuid


class LogRepository:
    def __init__(self, db):
        self.db = db
        self.cursor = self.db.cursor()

    def store(self, action, user_id, file_id):
        self.db.ping(reconnect=True)
        # membuat uuid untuk data log
        logId = str(uuid.uuid4())
        # membuat query insert ke table activity_log
        sql = "INSERT INTO activity_logs (id,action,user_id,file_id) VALUES (%s, %s, %s, %s)"
        # mengisi value yang akan diinsert
        vals = (logId, action, user_id, file_id)
        # execute query
        self.cursor.execute(sql, vals)

    def commit(self):
        self.db.ping(reconnect=True)
        # melakukan commit terhadap transaksi yang sudah dijalankan
        self.db.commit()

    def rollback(self):
        self.db.ping(reconnect=True)
        # melakukan rollback terhadap transaksi yang sudah dijalankan
        self.db.rollback()
