import xmlrpc.client as client
import json
server = client.ServerProxy(
    "http://127.0.0.1:1717/"
)

USERNAME = "admin"
PASSWORD = "admin"
UPLOAD_FILENAME = "sample.txt"
USER_UUID = "9e317ea2-1b37-44be-8bb0-47e110c9d907"
FILE_UUID = "2bd78b8b-802a-4939-aa33-68928e3b5b74"

# GET ALL LOG FILE

res = server.logs()
print(res)

# GET ALL DOWNLOAD LOG FILE

res = server.logs("download")
print(res)

# GET ALL UPLOAD LOG FILE

res = server.logs("upload")
print(res)

# REGISTER

res = server.register(USERNAME, PASSWORD)
print(res)

# LOGIN

res = server.login(USERNAME, PASSWORD)
print(res)

# GET FILE LIST

res = server.file_list()
print(res)

# GET MY FILE LIST

res = server.my_files(USER_UUID)
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
    print(res)
    if(res["success"]):
        filename = res["data"]["fileName"]
        with open(filename, "wb") as handle:
            handle.write(bytes(res["data"]['fileData'], 'utf-8'))
            handle.close()
    else:
        print(res)
except Exception as e:
    print(e)

# GET ALL MOST ACTIVE USERS

res = server.most_active()
print(res)

# GET ALL MOST ACTIVE DOWNLOAD USERS

res = server.most_active("download")
print(res)

# GET ALL MOST ACTIVE UPLOAD USERS

res = server.most_active("upload")
print(res)
