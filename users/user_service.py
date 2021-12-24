import hashlib
import uuid
from helper.json import *


class UserService:
    def __init__(self, userRepo):
        self.userRepo = userRepo

    def login(self, username, password):
        try:
            user = self.userRepo.findByUsername(username)
            if not user:
                return Response(success=False, message="Username tidak ditemukan")
            password = hashlib.md5(password.encode()).hexdigest()
            if user[3] != password:
                return Response(success=False, message="Password tidak sesuai")

            return Response(message="Berhasil login", data={
                "id": user[1],
                "username": user[2]
            })
        except Exception as e:
            return Response(
                success=False,
                message="Terjadi kesalahan, silahkan coba lagi nanti",
                error=e
            )

    def register(self, username, password):
        try:
            user = self.userRepo.findByUsername(username)
            if user:
                return Response(success=False, message="Username sudah digunakan")
            userId = str(uuid.uuid4())
            password = hashlib.md5(password.encode()).hexdigest()
            self.userRepo.store(userId, username, password)

            self.userRepo.commit()
            return Response(message="Registrasi berhasil")
        except Exception as e:
            self.userRepo.rollback()
            return Response(
                success=False,
                message="Terjadi kesalahan, silahkan coba lagi nanti",
                error=e
            )

    def get_most_active(self):
        try:
            users = self.userRepo.get_most_active_users()
            listuser = []
            for user in users:
                listuser.append({
                    "username": user[0],
                    "total": user[1],
                })
            return Response(
                message="Berhasil mendapatkan list user",
                data=listuser
            )
        except Exception as e:
            return Response(
                success=False,
                message="Terjadi kesalahan, silahkan coba lagi nanti",
                error=e
            )
