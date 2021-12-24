class UserRepository:
    def __init__(self, db):
        self.db = db
        self.cursor = self.db.cursor()

    def findByUsername(self, username):
        sql = 'SELECT * FROM users WHERE username = "{}"'.format(username)
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    def store(self, userId, username, password):
        sql = "INSERT INTO users (id,username,password) VALUES (%s, %s, %s)"
        vals = (userId, username, password)
        return self.cursor.execute(sql, vals)

    def get_most_active_users(self):
        sql = "SELECT u.username, COUNT(*) as total FROM users u JOIN activity_logs al ON al.user_id = u.id GROUP BY u.username ORDER BY total DESC"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def commit(self):
        self.db.commit()

    def rollback(self):
        self.db.rollback()
