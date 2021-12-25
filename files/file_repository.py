class FileRepository:
    def __init__(self, db):
        self.db = db
        self.cursor = self.db.cursor()

    def get_files(self):
        self.db.ping(reconnect=True)
        # membuat query untuk mendapatkan list file yang tersedia
        # join 2 table (user dan files)
        # kemudian diurutkan berdasarkan waktu file diupload
        sql = 'SELECT f.id, f.fileName, f.size, u.username, f.created_at, f.updated_at FROM files f JOIN users u ON f.user_id = u.id ORDER BY f.created_at DESC'
        # execute query
        self.cursor.execute(sql)
        # mengambil seluruh hasil query yang dijalankan
        return self.cursor.fetchall()

    def get_my_files(self, userId):
        self.db.ping(reconnect=True)
        # membuat query untuk mendapatkan list file dengan userId tertentu
        # join 2 table (user dan files)
        # kemudian diurutkan berdasarkan waktu file diupload
        sql = 'SELECT f.id, f.fileName, f.size, u.username, f.created_at, f.updated_at FROM files f JOIN users u ON f.user_id = u.id AND f.user_id = "{}" ORDER BY f.created_at DESC'.format(
            userId)
        # execute query
        self.cursor.execute(sql)
        # mengambil seluruh hasil query yang dijalankan
        return self.cursor.fetchall()

    def get_file_by_id(self, id):
        self.db.ping(reconnect=True)
        # membuat query untuk mendapatkan file dengan id tertentu
        sql = 'SELECT * FROM files WHERE id = "{}"'.format(id)
        # execute query
        self.cursor.execute(sql)
        # mengambil 1 data dari query yang dijalankan
        return self.cursor.fetchone()

    def store(self, fileId, userId, fileName, saved_filename, size):
        self.db.ping(reconnect=True)
        # membuat query insert ke table files
        sql = "INSERT INTO files (id, user_id,filename,saved_filename,size) VALUES (%s, %s, %s, %s, %s)"
        # mengisi value yang akan diinsert
        vals = (fileId, userId, fileName, saved_filename, size)
        # execute query
        return self.cursor.execute(sql, vals)

    def commit(self):
        self.db.ping(reconnect=True)
        # melakukan commit terhadap transaksi yang sudah dijalankan
        self.db.commit()

    def rollback(self):
        self.db.ping(reconnect=True)
        # melakukan rollback terhadap transaksi yang sudah dijalankan
        self.db.rollback()
