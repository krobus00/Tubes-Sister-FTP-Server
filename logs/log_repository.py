
import uuid


class LogRepository:
    def __init__(self, db):
        self.db = db
        self.cursor = self.db.cursor()

    def store(self, action, user_id, file_id):
        logId = str(uuid.uuid4())
        sql = "INSERT INTO activity_logs (id,action,user_id,file_id) VALUES (%s, %s, %s, %s)"
        vals = (logId, action, user_id, file_id)
        self.cursor.execute(sql, vals)

    def commit(self):
        self.db.commit()

    def rollback(self):
        self.db.rollback()
