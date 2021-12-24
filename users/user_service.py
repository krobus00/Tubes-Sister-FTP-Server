import hashlib
import uuid
from helper.json import *


class UserService:
    def __init__(self, userRepo):
        self.userRepo = userRepo

    def login(self, username, password):
        # membuat try catch untuk menghandle exception
        try:
            # memanggil fungsi find by username yang ada di user repository
            user = self.userRepo.findByUsername(username)
            # jika user tidak ditemukan
            if not user:
                # return pesan username tidak ditemukan
                return Response(success=False, message="Username tidak ditemukan")
            # melakukan hash md5 untuk atribut password
            password = hashlib.md5(password.encode()).hexdigest()
            # jika password tidak sama
            if user[3] != password:
                return Response(success=False, message="Password tidak sesuai")
            # return pesan berhasil dan detail user id serta username
            return Response(message="Berhasil login", data={
                "id": user[1],
                "username": user[2]
            })
        except Exception as e:
            # jika terjadi exception
            # return pesan error
            return Response(
                success=False,
                message="Terjadi kesalahan, silahkan coba lagi nanti",
                error=e
            )

    def register(self, username, password):
        # membuat try catch untuk menghandle exception
        try:
            # memanggil fungsi find by username yang ada di user repository
            user = self.userRepo.findByUsername(username)
            # jika username sudah ada
            if user:
                # menampilkan pesan error username sudah digunakan
                return Response(success=False, message="Username sudah digunakan")
            # membuat userId dengan menggunakan uuid
            userId = str(uuid.uuid4())
            # melakukan hashing password
            password = hashlib.md5(password.encode()).hexdigest()
            # memanggil fungsi store di user repository
            self.userRepo.store(userId, username, password)
            # commit transaksi dari user repository
            self.userRepo.commit()
            # return pesan sukses
            return Response(message="Registrasi berhasil")
        except Exception as e:
            # rollback transaksi user repository
            self.userRepo.rollback()
            # jika terjadi exception
            # return pesan error
            return Response(
                success=False,
                message="Terjadi kesalahan, silahkan coba lagi nanti",
                error=e
            )

    def get_most_active(self):
        # membuat try catch untuk menghandle exception
        try:
            # memanggil fungsi get most active users dari user repository
            users = self.userRepo.get_most_active_users()
            listuser = []
            # melakukan looping terhadap data users
            for user in users:
                # menambahkan data ke list users
                listuser.append({
                    "username": user[0],
                    "total": user[1],
                })
            # return pesan sukses
            return Response(
                message="Berhasil mendapatkan list user",
                data=listuser
            )
        except Exception as e:
            # jika terjadi exception
            # return pesan error
            return Response(
                success=False,
                message="Terjadi kesalahan, silahkan coba lagi nanti",
                error=e
            )
