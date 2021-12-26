class UserRepository:
    def __init__(self):
        self.db = None
        self.cursor = None

    def _database(self, db):
        self.db = db
        self.cursor = self.db.cursor()

    def findByUsername(self, db, username):
        self._database(db)
        # membuat query mendapatkan user dengan username tertentu
        sql = 'SELECT * FROM users WHERE username = "{}"'.format(username)
        # execute query
        self.cursor.execute(sql)
        # mengambil 1 data dari query yang dijalankan
        return self.cursor.fetchone()

    def store(self, db, userId, username, password):
        self._database(db)
        # membuat query insert ke table users
        sql = "INSERT INTO users (id,username,password) VALUES (%s, %s, %s)"
        # mengisi value yang akan diinsert
        vals = (userId, username, password)
        # execute query
        return self.cursor.execute(sql, vals)

    def get_most_active_users(self, db, filter):
        self._database(db)
        # membuat query untuk mengurutkan user berdasarkan total activity
        # join 2 table (user dan activity_logs)
        # kemudian group by username
        # kemudian diurutkan berdasarkan total activity_logs
        sql = "SELECT u.username, COUNT(*) as total FROM users u JOIN activity_logs al ON al.user_id = u.id"
        
        if filter == "upload":
            sql += " AND al.action = 'upload'"
        elif filter == "download":
            sql += " AND al.action = 'download'"

        sql += " GROUP BY u.username ORDER BY total DESC"
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
