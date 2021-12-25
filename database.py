import os
import mysql.connector
from mysql.connector import errorcode


class Database:
    def __init__(self):
        # membaca config database dari .env
        self.config = {
            'user': os.getenv('DB_USERNAME'),
            'password': os.getenv('DB_PASS'),
            'host': os.getenv('DB_HOST'),
            'database': os.getenv('DB_NAME'),
            'raise_on_warnings': True
        }
        self.db = None

    def connection(self):
        try:
            # membuat koneksi dari config yang sudah dibuat
            self.db = mysql.connector.connect(pool_name = "tubes",
                              pool_size = 10,
                              **self.config)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                # menampilkan pesan error ketika credensial tidak sesuai
                exit("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                # menampilkan pesan error ketika database tidak ditemukan
                exit("Database does not exist")
            else:
                # menampilkan pesan error jika ada error lainnya
                print(err)
        else:
            return self.db

    def close_connection(self):
        if self.db.is_connected():
            # self.db.cursor.close()
            self.db.close()
