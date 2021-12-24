import xmlrpc.client as client
import json
server = client.ServerProxy(
    "http://127.0.0.1:1717/"
)

USERNAME = "username"
PASSWORD = "password"
UPLOAD_FILENAME = "sample.txt"
USER_UUID = "39493e92-b400-406c-a2d1-9b1408f2eaf9"
FILE_UUID = "544791cc-2d78-4222-ad41-2d38ba7a94b8"

# REGISTER

res = server.register(USERNAME, PASSWORD)
print(res)

# LOGIN

res = server.login(USERNAME, PASSWORD)
print(res)

# GET FILE LIST

res = server.file_list()
print(res)

# UPLOAD

try:
    filename = UPLOAD_FILENAME
    with open(filename, "rb") as handle:
        data = client.Binary(handle.read())
        res = server.file_upload(data, filename, USER_UUID)
        print(res)
except Exception as e:
    print(e)


# DOWNLOAD

try:
    res = server.file_download(USER_UUID, FILE_UUID)
    res = json.loads(res)
    if(res["success"]):
        filename = res["data"]["fileName"]
        with open(filename, "wb") as handle:
            handle.write(bytes(res["data"]['fileData'], 'utf-8'))
            handle.close()
    else:
        print(res)
except Exception as e:
    print(e)

# GET MOST ACTIVE USERS

res = server.most_active()
print(res)
