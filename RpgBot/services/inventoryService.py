from models.character import Character
from services.cacheService import SimpleCache
from data.dataContext import Context, CharacterTable
from sqlalchemy.orm import Session
from sqlalchemy import update

class InventoryService():
    def __init__(self, db: Context, cache: SimpleCache):
        self.db = db.engine
        self.cache = cache
        return

    
    async def ShowInventorySimple(self, player:str):
        character = self.cache.get(player)

        inv = character.Inventory

        return {
            "Gold": inv.Gold,
            "Equipped": [item.Name for item in inv.Equipped],
            "Stored": [item.Name for item in inv.Stored],
            "Ability": [item.Name for item in inv.Ability]
        }


    async def UnequipItem(self, player:str, itemName:str):
        character = self.cache.get(player)

        if character.Inventory.Stored.count == character.MaxInventory:
            return {
                "Error": "No room in stored inventory"
            }

        itemToUnequip = list(filter(lambda i: i.Name == itemName, character.Inventory.Equipped))
        if len(itemToUnequip) == 0:
            return {
                "Error": "Item doesn't exist in equipped inventory"
            }

        character.Inventory.Equipped = [item for item in character.Inventory.Equipped if item.Name != itemName]
        character.Inventory.Stored.append(itemToUnequip[0])
        
        character.Inventory.checkInventoryForDuplicates()

        session = Session(bind = self.db)
        chTable = character.ToCharacterTable(player)

        statement = update(CharacterTable).where(CharacterTable.playerName == player).values(inventory = chTable.inventory)
        session.execute(statement)
        session.commit()
        session.close()

        character.deriveStats()
        self.cache.set(player, character)

        return

    async def EquipItem(self, player:str, itemName:str):
        character = self.cache.get(player)

        itemToEquip = list(filter(lambda i: i.Name == itemName, character.Inventory.Stored))
        if len(itemToEquip) == 0:
            return {
                "Error": "No item of that name in inventory"    
            }

        itemType = itemToEquip[0].Type
        #check to see if type is already equipped
        slotIsFree = False
        if itemType == "Hand":
            slotIsFree = len(list(filter(lambda i: i.Type == itemType, character.Inventory.Equipped))) < 2
        else:
            slotIsFree = len(list(filter(lambda i: i.Type == itemType, character.Inventory.Equipped))) == 0
        
        if slotIsFree == False:
            return {
                "Error": f"Slot unavailable. Unequip item in {itemType}"   
            }

        character.Inventory.Stored = [item for item in character.Inventory.Stored if item.Name != itemName]
        character.Inventory.Equipped.append(itemToEquip[0])

        
        character.Inventory.checkInventoryForDuplicates()

        session = Session(bind = self.db)
        chTable = character.ToCharacterTable(player)

        statement = update(CharacterTable).where(CharacterTable.playerName == player).values(inventory = chTable.inventory)
        session.execute(statement)
        session.commit()
        session.close()

        character.deriveStats()
        self.cache.set(player, character)

        return

    async def DiscardItem(self, player:str, itemName:str):
        character = self.cache.get(player) or Character()

        itemToDrop = list(filter(lambda i: i.Name == itemName, character.Inventory.Stored))
        if len(itemToDrop) == 0:
            return {
                "Error": "No item of that name in inventory"    
            }

        character.Inventory.Stored = [item for item in character.Inventory.Stored if item.Name != itemName]
        character.Inventory.checkInventoryForDuplicates()

        session = Session(bind = self.db)
        chTable = character.ToCharacterTable(player)

        statement = update(CharacterTable).where(CharacterTable.playerName == player).values(inventory = chTable.inventory)
        session.execute(statement)
        session.commit()
        session.close()

        self.cache.set(player, character)

        return
    
    async def GiveGold(self, player:str, targetPlayer:str, amount:int):
        ch = self.cache.get(player)
        target = self.cache.get(targetPlayer)

        playerGold = ch.Inventory.Gold
        if playerGold < amount:
            return {
                "Error": "Insufficient gold to give"    
            }

        ch.Inventory.Gold -= amount
        target.Inventory.Gold += amount

        session = Session(bind = self.db)
        try:
            chTable = ch.ToCharacterTable(player)
            statement = update(CharacterTable).where(CharacterTable.playerName == player).values(inventory = chTable.inventory)
            session.execute(statement)

            targetTable = target.ToCharacterTable(targetPlayer)
            statement = update(CharacterTable).where(CharacterTable.playerName == targetPlayer).values(inventory = targetTable.inventory)
            session.execute(statement)

            session.commit()
            self.cache.set(player, ch)
            self.cache.set(targetPlayer, target)
        except Exception as ex:
            print(ex)
            return {
                "Error": "Trade could not be completed"    
            }
            session.rollback()
        session.close()

        return

    async def GiveItem(self, player:str, targetPlayer:str, itemName:str):
        ch = self.cache.get(player)
        target = self.cache.get(targetPlayer)

        itemToGive = list(filter(lambda i: i.Name == itemName, ch.Inventory.Stored))
        if len(itemToGive) == 0:
            return {
                "Error": "No item of that name in inventory"    
            }

        ch.Inventory.Stored = [item for item in ch.Inventory.Stored if item.Name != itemName]
        target.Inventory.Stored.append(itemToGive[0])
        target.Inventory.checkInventoryForDuplicates()

        session = Session(bind = self.db)
        try:
            chTable = ch.ToCharacterTable(player)
            statement = update(CharacterTable).where(CharacterTable.playerName == player).values(inventory = chTable.inventory)
            session.execute(statement)

            targetTable = target.ToCharacterTable(player)
            statement = update(CharacterTable).where(CharacterTable.playerName == targetPlayer).values(inventory = targetTable.inventory)
            session.execute(statement)

            session.commit()
            self.cache.set(player, ch)
            self.cache.set(targetPlayer, target)
        except Exception as ex:
            print(ex)
            return {
                "Error": "Trade could not be completed"    
            }
            session.rollback()
        session.close()

        return

    async def RenameItem(self, player:str, itemName:str, newItemName:str):
        character = self.cache.get(player)

        itemToRename = list(filter(lambda i: i.Name == itemName, character.Inventory.Stored))
        if len(itemToRename) == 0:
            return {
                "Error": "No item of that name in stored inventory"    
            }

        itemToRename[0].Name = newItemName
        character.Inventory.checkInventoryForDuplicates()

        session = Session(bind = self.db)
        chTable = character.ToCharacterTable(player)

        statement = update(CharacterTable).where(CharacterTable.playerName == player).values(inventory = chTable.inventory)
        session.execute(statement)
        session.commit()
        session.close()

        self.cache.set(player, character)