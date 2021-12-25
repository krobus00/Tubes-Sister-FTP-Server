from dotenv import load_dotenv

from database import Database
from files.file_repository import FileRepository
from files.file_service import FileService
from logs.log_repository import LogRepository
from rpc_server import RPCServer
from users.user_repository import UserRepository
from users.user_service import UserService


def main():
    # load .env
    load_dotenv()
    # membuat koneksi database baru
    db = Database()

    # membuat file repository
    file_repository = FileRepository()
    # membuat user repository
    user_repository = UserRepository()
    # membuat log repository
    log_repository = LogRepository()

    # membuat file service
    file_service = FileService(db, file_repository, log_repository)
    # membuat user service
    user_service = UserService(db, user_repository)
    # membuat server
    server = RPCServer(user_service, file_service)
    # menjalankan server
    server.run()
    # menutup koneksi database ketika exit program
    db.close()


if __name__ == "__main__":
    main()
