import xmlrpc.client as client
import json
server = client.ServerProxy(
    "http://127.0.0.1:1717/"
)

USERNAME = "username"
PASSWORD = "password"
UPLOAD_FILENAME = "sample.txt"
USER_UUID = "15154628-ee70-496c-8c85-80d965207bb9"
FILE_UUID = "4f321183-bbeb-45e3-a139-173d54d474e3"

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
