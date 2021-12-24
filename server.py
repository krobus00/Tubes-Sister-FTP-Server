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
    db = Database().connection()

    # membuat file repository
    file_repository = FileRepository(db)
    # membuat user repository
    user_repository = UserRepository(db)
    # membuat log repository
    log_repository = LogRepository(db)

    # membuat file service
    file_service = FileService(file_repository, log_repository)
    # membuat user service
    user_service = UserService(user_repository)
    # membuat server
    server = RPCServer(user_service, file_service)
    # menjalankan server
    server.run()
    # menutup koneksi database ketika exit program
    db.close()


if __name__ == "__main__":
    main()
