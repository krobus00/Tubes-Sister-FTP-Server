import uuid
from datetime import datetime

from helper.json import *


class FileService:
    def __init__(self, db, fileRepo, logRepo):
        self.db = db
        self.conn = self.db.connection()
        self.fileRepo = fileRepo
        self.logRepo = logRepo

    def upload(self, fileData, fileName, userId):
        # membuat try catch untuk menghandle exception
        try:
            self.conn = self.db.connection()
            # membuat format nama file dengan tanggal dan jam
            # agar file tidak duplikat
            saved_filename = "{}_{}".format(
                datetime.now().strftime("%y%m%d_%H%M%S"),
                fileName,
            )
            # write data ke folder upload
            with open("uploads/{}".format(saved_filename), "wb") as handle:
                # melakukan write data
                handle.write(fileData.data)
                # generate uuid
                fileId = str(uuid.uuid4())
                # menyimpan nama file dan ukuran file ke database
                self.fileRepo.store(self.conn, fileId, userId, fileName,
                                    saved_filename, handle.tell())
                # mencatat history dari user sekarang
                self.logRepo.store(self.conn, "UPLOAD", userId, fileId)

                # commit transaction ketika semua data sudah berhasil diinput
                self.fileRepo.commit(self.conn)
                self.logRepo.commit(self.conn)
                self.db.close_connection()
                handle.close()
                # mengembalikan nilai True karena fungsi berjalan normal
                return Response(message="Data berhasil diupload")
        except Exception as e:
            # ketika ada fungsi yang gagal maka rollback transaction yang sudah berjalan
            self.fileRepo.rollback(self.conn)
            self.logRepo.rollback(self.conn)
            self.db.close_connection()
            # return error karena fungsi terjadi exception
            return Response(
                message="Terjadi kesalahan, silahkan coba lagi nanti",
                error=e
            )

    def download(self, userId, fileId):
        # membuat try catch untuk menghandle exception
        try:
            self.conn = self.db.connection()
            # memanggil get file by id dari file repo
            file = self.fileRepo.get_file_by_id(self.conn, fileId)
            # jika file tidak ditemukan
            if not file:
                # return pesan file tidak ditemukan
                return Response(
                    success=False,
                    message="File tidak ditemukan!"
                )
            # membaca file yang dipilih
            with open("uploads/{}".format(file[4]), "rb") as handle:
                # mencatat history dari user sekarang
                self.logRepo.store(self.conn, "DOWNLOAD", userId, fileId)
                # commit transaction ketika semua data sudah berhasil diinput
                self.logRepo.commit(self.conn)
                # return pesan sukses dengan filename dan filedatanya
                self.db.close_connection()
                fileData = handle.read().decode('utf8')
                handle.close()
                return Response(
                    message="Berhasil melakukan download data",
                    data={
                        "fileName": file[3],
                        "fileData": fileData,
                    }
                )
        except Exception as e:
            # ketika ada fungsi yang gagal maka rollback transaction yang sudah berjalan
            self.logRepo.rollback()
            self.db.close_connection()
            # jika terjadi exception
            # return pesan error
            return Response(
                success=False,
                message="Terjadi kesalahan, silahkan coba lagi nanti",
                error=e
            )

    def get_list_file(self):
        # membuat try catch untuk menghandle exception
        try:
            self.conn = self.db.connection()
            # memanggil fungsi get files dari file repository
            files = self.fileRepo.get_files(self.conn)
            listfiles = []
            # melakukan looping files yang didapatkan
            for file in files:
                # menambahkan data ke list files
                listfiles.append({
                    "id": file[0],
                    "fileName": file[1],
                    "size": file[2],
                    "username": file[3],
                    "createdAt": file[4].strftime('%Y-%m-%d %H:%M:%S'),
                })
            self.db.close_connection()
            # return pesan berhasil
            return Response(
                message="Berhasil mendapatkan list file",
                data=listfiles
            )
        except Exception as e:
            self.db.close_connection()
            # jika terjadi exception
            # return pesan error
            return Response(
                success=False,
                message="Terjadi kesalahan, silahkan coba lagi nanti",
                error=e
            )

    def get_my_files(self, userId):
        # membuat try catch untuk menghandle exception
        try:
            self.conn = self.db.connection()
            # memanggil fungsi get my files dari file repository
            files = self.fileRepo.get_my_files(self.conn, userId)
            listfiles = []
            # melakukan looping files yang didapatkan
            for file in files:
                listfiles.append({
                    "id": file[0],
                    "fileName": file[1],
                    "size": file[2],
                    "username": file[3],
                    "createdAt": file[4].strftime('%Y-%m-%d %H:%M:%S'),
                })
            self.db.close_connection()
            # return pesan berhasil
            return Response(
                message="Berhasil mendapatkan list file",
                data=listfiles
            )
        except Exception as e:
            self.db.close_connection()
            # jika terjadi exception
            # return pesan error
            return Response(
                success=False,
                message="Terjadi kesalahan, silahkan coba lagi nanti",
                error=e
            )
    def get_log_activity(self, filter=""):
        # membuat try catch untuk menghandle exception
        try:
            self.conn = self.db.connection()
            # memanggil fungsi get activity log dari log repository
            logs = self.logRepo.get_activity_log(self.conn, filter)
            listlogs = []
            # melakukan looping terhadap data log
            for log in logs:
                # menambahkan data ke list logs
                listlogs.append({
                    "tanggal": log[0].strftime('%Y-%m-%d'),
                    "total": log[1],
                })
            self.db.close_connection()
            # return pesan sukses
            return Response(
                message="Berhasil mendapatkan data log",
                data=listlogs
            )
        except Exception as e:
            self.db.close_connection()
            # jika terjadi exception
            # return pesan error
            return Response(
                success=False,
                message="Terjadi kesalahan, silahkan coba lagi nanti",
                error=e
            )
