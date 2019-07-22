import json
from typing import Dict
import TokenType
import Attack

attacks = {}
tokens = {}

def load(filename="data.json"):
    with open(filename) as data_file:
        data = json.load(data_file)
    for a in data["Attacks"]:
        attacks[a["name"]] = Attack.Attack(**a)
    assert len(attacks) == len(data["Attacks"])
    for t in data["Tokens"]:
        tokens[t["name"]] = TokenType.TokenType.from_json(**t)
    assert len(tokens) == len(data["Tokens"])
