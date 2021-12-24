class FileRepository:
    def __init__(self, db):
        self.db = db
        self.cursor = self.db.cursor()

    def get_files(self):
        sql = 'SELECT f.id, f.fileName, f.size, u.username, f.created_at, f.updated_at FROM files f JOIN users u ON f.user_id = u.id'
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def get_my_files(self, userId):
        sql = 'SELECT f.id, f.fileName, f.size, u.username, f.created_at, f.updated_at FROM files f JOIN users u ON f.user_id = u.id AND f.user_id = "{}"'.format(
            userId)
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def get_file_by_id(self, id):
        sql = 'SELECT * FROM files WHERE id = "{}"'.format(id)
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    def store(self, fileId, userId, fileName, saved_filename, size):
        sql = "INSERT INTO files (id, user_id,filename,saved_filename,size) VALUES (%s, %s, %s, %s, %s)"
        vals = (fileId, userId, fileName, saved_filename, size)
        return self.cursor.execute(sql, vals)
        # self.db.commit()

    def commit(self):
        self.db.commit()

    def rollback(self):
        self.db.rollback()
