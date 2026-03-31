import json


def to_json(result):
    return json.dumps(result, ensure_ascii=False, indent=2)
