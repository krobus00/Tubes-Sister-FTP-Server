import xmlrpc.client as client
import json
import base64

server = client.ServerProxy(
    "http://127.0.0.1:1818/"
)

USERNAME = "admin"
PASSWORD = "admin"
UPLOAD_FILENAME = "sample.txt"
USER_UUID = "9e317ea2-1b37-44be-8bb0-47e110c9d907"
FILE_UUID = "00c0e99b-2a48-4188-9826-9a42d34048ff"


# GET ALL USERS
res = server.get_users()
print(res)


# GET ALL LOG FILE

res = server.log_data()
print(res)

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
            handle.write(base64.b64decode(res["data"]['fileData']))
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

# GET ALL ACTIVITY LOGS

res = server.logs()
print(res)

# GET ALL DOWNLOAD ACTIVITY LOGS

res = server.logs("download")
print(res)

# GET ALL UPLOAD ACTIVITY LOGS

res = server.logs("upload")
print(res)
