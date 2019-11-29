import random

categoryL = ['Weapon', 'Jewels', 'Head', 'Chest', 'Pants', 'Arms', 'Legs']


class Item:

    def __init__(self, name, description="", price=0):
        """
        :param name: "self"'s name
        :param description: "self"'s description
        :param price: "self"'s price
        """
        self.name = name
        self.description = description
        self.price = price


class Equipment(Item):
    """
    function to equip an item
    """
    def __init__(self, name, description, category, price=1, mini_level=1, power=[1, 0], dodge=0, parry=0, trait=[0, 0], stats=[0, 0]):
        super().__init__(name, description, price)
        self.equiped = False
        self.category = category
        self.mini_level = mini_level
        self.power = power
        self.dodge_chance = dodge
        self.parry_chance = parry
        self.special_trait = trait
        self.special_stats = stats


class Consumable(Item):
    """
    function to use a consumable item
    """
    def __init__(self, name, description, price, effect):

        super().__init__(name, description, price)
        self.effect = effect

    def used(self):
        self.effect()


def none():
    pass
