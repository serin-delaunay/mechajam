import json
import Attack
import TokenType

attacks = {}
tokens = {}
info = {"Attack": {}, "Token": {}}


def load(filename="data.json"):
    with open(filename) as data_file:
        data = json.load(data_file)
    for a in data["Attacks"]:
        attacks[a["name"]] = Attack.Attack.from_json(**a)
    assert len(attacks) == len(data["Attacks"])
    for t in data["Tokens"]:
        tokens[t["name"]] = TokenType.TokenType.from_json(**t)
    assert len(tokens) == len(data["Tokens"])
