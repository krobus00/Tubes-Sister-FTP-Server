import uuid
from datetime import datetime

from helper.json import *


class FileService:
    def __init__(self, fileRepo, logRepo):
        self.fileRepo = fileRepo
        self.logRepo = logRepo

    def upload(self, fileData, fileName, userId):
        # membuat try catch untuk menghandle exception
        try:
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
                self.fileRepo.store(fileId, userId, fileName,
                                    saved_filename, handle.tell())
                # mencatat history dari user sekarang
                self.logRepo.store("UPLOAD", userId, fileId)

                # commit transaction ketika semua data sudah berhasil diinput
                self.fileRepo.commit()
                self.logRepo.commit()
                # mengembalikan nilai True karena fungsi berjalan normal
                return Response(message="Data berhasil diupload")
        except Exception as e:
            # ketika ada fungsi yang gagal maka rollback transaction yang sudah berjalan
            self.fileRepo.rollback()
            self.logRepo.rollback()
            # return error karena fungsi terjadi exception
            return Response(
                message="Terjadi kesalahan, silahkan coba lagi nanti",
                error=e
            )

    def download(self, userId, fileId):
        # memanggil get file by id dari file repo
        file = self.fileRepo.get_file_by_id(fileId)
        # jika file tidak ditemukan
        if not file:
            # return pesan file tidak ditemukan
            return Response(
                success=False,
                message="File tidak ditemukan!"
            )
        # membuat try catch untuk menghandle exception
        try:
            # membaca file yang dipilih
            with open("uploads/{}".format(file[4]), "rb") as handle:
                # mencatat history dari user sekarang
                self.logRepo.store("DOWNLOAD", userId, fileId)
                # return pesan sukses dengan filename dan filedatanya
                return Response(
                    message="Berhasil melakukan download data",
                    data={
                        "fileName": file[3],
                        "fileData": handle.read().decode('utf8'),
                    }
                )
        except Exception as e:
            # ketika ada fungsi yang gagal maka rollback transaction yang sudah berjalan
            self.logRepo.rollback()
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
            # memanggil fungsi get files dari file repository
            files = self.fileRepo.get_files()
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
            # return pesan berhasil
            return Response(
                message="Berhasil mendapatkan list file",
                data=listfiles
            )
        except Exception as e:
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
            # memanggil fungsi get my files dari file repository
            files = self.fileRepo.get_my_files(userId)
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
            # return pesan berhasil
            return Response(
                message="Berhasil mendapatkan list file",
                data=listfiles
            )
        except Exception as e:
            # jika terjadi exception
            # return pesan error
            return Response(
                success=False,
                message="Terjadi kesalahan, silahkan coba lagi nanti",
                error=e
            )
