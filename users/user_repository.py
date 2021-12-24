class UserRepository:
    def __init__(self, db):
        self.db = db
        self.cursor = self.db.cursor()

    def findByUsername(self, username):
        # membuat query mendapatkan user dengan username tertentu
        sql = 'SELECT * FROM users WHERE username = "{}"'.format(username)
        # execute query
        self.cursor.execute(sql)
        # mengambil 1 data dari query yang dijalankan
        return self.cursor.fetchone()

    def store(self, userId, username, password):
        # membuat query insert ke table users
        sql = "INSERT INTO users (id,username,password) VALUES (%s, %s, %s)"
        # mengisi value yang akan diinsert
        vals = (userId, username, password)
        # execute query
        return self.cursor.execute(sql, vals)

    def get_most_active_users(self):
        # membuat query untuk mengurutkan user berdasarkan total activity
        # join 2 table (user dan activity_logs)
        # kemudian group by username
        # kemudian diurutkan berdasarkan total activity_logs
        sql = "SELECT u.username, COUNT(*) as total FROM users u JOIN activity_logs al ON al.user_id = u.id GROUP BY u.username ORDER BY total DESC"
        # execute query
        self.cursor.execute(sql)
        # mengambil seluruh hasil query yang dijalankan
        return self.cursor.fetchall()

    def commit(self):
        # melakukan commit terhadap transaksi yang sudah dijalankan
        self.db.commit()

    def rollback(self):
        # melakukan rollback terhadap transaksi yang sudah dijalankan
        self.db.rollback()
