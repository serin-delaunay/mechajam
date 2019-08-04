from TokenState import TokenState
from Data import attacks


class AttackResolver:
    def __init__(self, attacker, defender):
        self.attack_index = 0
        self.token_index = 0
        self.attacker = attacker
        self.attacks = self.attacker.get_attacks()
        self.defender = defender

    def resolve_contest(self):
        attack = self.attacks[self.attack_index]
        token = self.defender.health_tokens[self.token_index]
        if token.state is TokenState.damaged:
            self.token_index += 1
        elif attack.name is "Pierce" and self.token_index < len(self.defender.health_tokens()) - 1:
            self.token_index += 1
            self.attacks[self.attack_index] = attacks["Attack"]
        elif token.type.name is "Armour" and attack.name is not "Heavy":
            self.attack_index += 1
        else:
            token.state = TokenState.damaged
            self.token_index += 1
            self.attack_index += 1

    def resolve_combat(self):
        while not self.stop():
            self.resolve_contest()

    def stop(self):
        return self.attack_index >= len(self.attacks) or self.token_index >= len(self.defender.health_tokens)
