import os
from xmlrpc.server import SimpleXMLRPCServer


class RPCServer:
    def __init__(self, userService, fileService):
        self.userService = userService
        self.fileService = fileService
        self.server = None

    def run(self):
        self.server = SimpleXMLRPCServer(
            ("0.0.0.0", int(os.getenv('APP_PORT'))), allow_none=True
        )
        print("SERVER RUNNING")
        self.server.register_introspection_functions()

        # files
        self.server.register_function(
            self.fileService.upload,
            "file_upload"
        )

        self.server.register_function(
            self.fileService.download,
            "file_download"
        )

        self.server.register_function(
            self.fileService.get_list_file,
            "file_list"
        )

        self.server.register_function(
            self.fileService.get_my_files,
            "my_files"
        )

        # users
        self.server.register_function(
            self.userService.register,
            "register"
        )
        self.server.register_function(
            self.userService.login,
            "login"
        )

        self.server.register_function(
            self.userService.get_most_active,
            "most_active"
        )
        self.server.serve_forever()
