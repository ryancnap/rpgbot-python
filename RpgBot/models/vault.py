from data.dataContext import VaultTable
from models.character import Inventory

class Vault():
    def __init__(self, CharacterId:int=0, Inventory:str="{}"):
        self.CharacterId = CharacterId
        self.Inventory = Inventory
        return

    def to_dict(self):
        return {
            "CharacterId": self.CharacterId,
            "Inventory": self.Inventory.to_dict
        }