import uuid
from datetime import datetime

from helper.json import *


class FileService:
    def __init__(self, fileRepo, logRepo):
        self.fileRepo = fileRepo
        self.logRepo = logRepo

    def upload(self, fileData, fileName, userId):
        try:
            saved_filename = "{}_{}".format(
                datetime.now().strftime("%y%m%d_%H%M%S"),
                fileName,
            )
            with open("uploads/{}".format(saved_filename), "wb") as handle:
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
        file = self.fileRepo.get_file_by_id(fileId)
        if not file:
            return Response(
                success=False,
                message="File tidak ditemukan!"
            )
        try:
            with open("uploads/{}".format(file[4]), "rb") as handle:
                # mencatat history dari user sekarang
                self.logRepo.store("DOWNLOAD", userId, fileId)
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
            return Response(
                success=False,
                message="Terjadi kesalahan, silahkan coba lagi nanti",
                error=e
            )

    def get_list_file(self):
        try:
            files = self.fileRepo.get_files()
            listfiles = []
            for file in files:
                listfiles.append({
                    "id": file[0],
                    "fileName": file[1],
                    "size": file[2],
                    "username": file[3],
                    "createdAt": file[4].strftime('%Y-%m-%d %H:%M:%S'),
                })
            return Response(
                message="Berhasil mendapatkan list file",
                data=listfiles
            )
        except Exception as e:
            return Response(
                success=False,
                message="Terjadi kesalahan, silahkan coba lagi nanti",
                error=e
            )
