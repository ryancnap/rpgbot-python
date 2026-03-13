import random
import time

class Character:
    #default constructor
    def __init__(self):
        #inherent stats
        self.Name = ""
        self.Strength = 0
        self.Dexterity = 0
        self.Endurance = 0
        self.Intelligence = 0
        self.Faith = 0
        self.Luck = 0

        #derived stats
        self.AttackRating = 0
        self.DamageReduction = 0
        self.SpellDamage = 0
        self.MaxHP = 0
        self.CurrentHP = 0
        self.MaxAP = 0
        self.CurrentAP = 0
        self.Evasion = 0
        self.MaxInventory = 0
        self.MaxAbilities = 0
        self.CritChance = 0

        #inventory
        self.Inventory = Inventory()

    #Make a new character
    def new(self, name:str):
        self.Name = name
        self.Strength = self._rollStat()
        self.Dexterity = self._rollStat()
        self.Endurance = self._rollStat()
        self.Intelligence = self._rollStat()
        self.Faith = self._rollStat()
        self.Luck = self._rollStat()

        return self

    #required for JSON dump
    def to_dict(self):
        return {
            "Name": self.Name,
            "Strength": self.Strength,
            "Dexterity": self.Dexterity,
            "Endurance": self.Endurance,
            "Intelligence": self.Intelligence,
            "Faith": self.Faith,
            "Luck": self.Luck,
            "AttackRating": self.AttackRating,
            "DamageReduction": self.DamageReduction,
            "SpellDamage": self.SpellDamage,
            "Evasion": self.Evasion,
            "CritChance": self.CritChance,
            "InventorySpace": self.MaxInventory,
            "MaxAbilities": self.MaxAbilities,
            "MaxHP": self.MaxHP,
            "CurrentHP": self.CurrentHP,
            "MaxAP": self.MaxAP,
            "CurrentAP": self.CurrentAP,
            "Inventory": {
                "Equipped":[item.to_dict() for item in self.Inventory.Equipped],
                "Stored": [item.to_dict() for item in self.Inventory.Stored],
                "Ability": [item.to_dict() for item in self.Inventory.Ability],
            }
        }

    #Private method. Used to determine stat
    def _rollStat(self):
        #refresh seed based on nanosecond time
        random.seed(time.time_ns())
        #range 3-16 simulates a 3d6 roll
        return random.randint(3,18)
#end class def


class Inventory():
    def __init__(self):
        self.Equipped = [] #list of loot
        self.Stored = [] #list of loot
        self.Ability = [] #list of abilities

    def to_dict(self):
        return {
            "Equipped": self.Equipped,
            "Stored": self.Stored,
            "Ability": self.Ability
        }