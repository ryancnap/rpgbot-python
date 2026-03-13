import json


class Loot():
    def __init__(self):
        self.Name = ""
        self.Description = ""
        self.Type = ""
        self.Effects = Effect()

    def to_dict(self):
        return {
            "Name": self.Name,
            "Description": self.Description,
            "Type": self.Type,
            "Effects": self.Effects.to_dict()
        }

class Effect():
    def __init__(self, Type:str="", AttackRating:int=0, DamageReduction:int=0, Evasion:int=0, Heal:int=0, CritChance:int=0, SpellDamage:int=0, MaxHP:int=0, MaxAP:int=0, Use:list=[]):
        self.Type = Type
        self.AttackRating = AttackRating
        self.DamageReduction = DamageReduction
        self.Evasion = Evasion
        self.Heal = Heal
        self.CritChance = CritChance
        self.SpellDamage = SpellDamage
        self.MaxHP = MaxHP
        self.MaxAP = MaxAP
        self.Use = Use

    def to_dict(self):
        return {
            "Type": self.Type,
            "AttackRating": self.AttackRating,
            "DamageReduction": self.DamageReduction,
            "Evasion": self.Evasion,
            "Heal": self.Heal,
            "CritChance": self.CritChance,
            "SpellDamage": self.SpellDamage,
            "MaxHP": self.MaxHP,
            "MaxAP": self.MaxAP,
            "Use": self.Use
        }