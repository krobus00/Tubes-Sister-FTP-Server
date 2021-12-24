
import json
import os


def IsProductionEnv():
    return os.getenv('ENV') == "production"


def Response(success=True, message="", data=None, error=None):
    res = {
        "success": success,
        "message": message,
        "data": data,
    }
    if not IsProductionEnv():
        res["errorTraceback"] = str(error)

    return json.dumps(res)


def DecodeJson(payload):
    return json.loads(payload)

