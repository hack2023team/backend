import json

def dump_to_text(l:list) -> str:
    return json.dumps(l)

def dump_to_list(s: str) -> list:
    return json.loads(s)
