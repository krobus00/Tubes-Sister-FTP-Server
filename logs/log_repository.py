
import uuid


class LogRepository:
    def __init__(self):
        self.db = None
        self.cursor = None

    def _database(self, db):
        self.db = db
        self.cursor = self.db.cursor()

    def store(self, db, action, user_id, file_id):
        self._database(db)
        # membuat uuid untuk data log
        logId = str(uuid.uuid4())
        # membuat query insert ke table activity_log
        sql = "INSERT INTO activity_logs (id,action,user_id,file_id) VALUES (%s, %s, %s, %s)"
        # mengisi value yang akan diinsert
        vals = (logId, action, user_id, file_id)
        # execute query
        self.cursor.execute(sql, vals)

    def get_activity_log(self, db, filter):
        self._database(db)
        # membuat query untuk mengambil data log berdasarkan tanggal
        sql = "SELECT DATE(created_at) AS tanggal, COUNT(*) AS total FROM activity_logs"
        
        if filter == "upload":
            sql += " WHERE action = 'upload'"
        elif filter == "download":
            sql += " WHERE action = 'download'"
        
        sql += " GROUP BY DATE(created_at) ORDER BY tanggal DESC"

        # execute query
        self.cursor.execute(sql)
        # mengambil seluruh hasil query yang dijalankan
        return self.cursor.fetchall()

    def commit(self, db):
        self._database(db)
        # melakukan commit terhadap transaksi yang sudah dijalankan
        self.db.commit()

    def rollback(self, db):
        self._database(db)
        # melakukan rollback terhadap transaksi yang sudah dijalankan
        self.db.rollback()
