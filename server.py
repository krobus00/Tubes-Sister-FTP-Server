from dotenv import load_dotenv

from database import Database
from files.file_repository import FileRepository
from files.file_service import FileService
from logs.log_repository import LogRepository
from rpc_server import RPCServer
from users.user_repository import UserRepository
from users.user_service import UserService


def main():
    load_dotenv()
    db = Database().connection()

    file_repository = FileRepository(db)
    user_repository = UserRepository(db)
    log_repository = LogRepository(db)

    file_service = FileService(file_repository, log_repository)
    user_service = UserService(user_repository)
    server = RPCServer(user_service, file_service)

    server.run()
    db.close()


if __name__ == "__main__":
    main()
