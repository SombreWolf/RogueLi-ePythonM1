import random

items = ['branch', 'wood shield', 'meat', 'iron axe', 'iron shield', 'bubble']

categoryL = ['Weapon', 'Jewels', 'Head', 'Chest', 'Pants', 'Arms', 'Legs']

prices = [2, 2, 1, 5, 5, 1]

equipables = [3, 2, -1, 3, 2, -1]

powers = [1, 0, 0, 2, 0, 0]

armors = [0, 1, 0, 0, 2, 0]


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
    def __init__(self, name, description, category, price=1, mini_level=1, power=[0, 0], dodge=0, parry=0, trait=[0, 0], stats=[0, 0]):
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
    def __init__(self, name, description, price, effect):

        super().__init__(name, description, price)
        self.effect = effect

    def used(self):
        self.effect()


def none():
    pass
