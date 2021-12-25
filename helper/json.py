
import json
import os


def IsProductionEnv():
    # melakukan pengecekan environment
    return os.getenv('ENV') == "production"


def Response(success=True, message="", data=None, error=None):
    # membuat fungsi response builder agar response konsisten
    res = {
        "success": success,
        "message": message,
        "data": data,
    }
    # menambahkan error traceback jika env bukan production
    # agar mempermudah debugging
    if not IsProductionEnv():
        res["traceback"] = str(error)
    # return string json
    return json.dumps(res)
