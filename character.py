import inventory
import random

pieces = ['head',
          'hands',
          'left hand',
          'right hand',
          'upper body',
          'legs',
          'feet']

categoryL = ["player", "Monster", "Merchant"]


class Character:

    def __init__(self, name="Mob", category="None", health=10, strength=5, position=[0, 0]):
        # TODO condition on category
        self.name = name
        self.category = category
        self.health = health
        self.health_max = health
        self.shield_point = 0
        self.dodge_chance = 0
        self.parry_chance = 0
        self.critic_chance = random.randint(0, 5)
        self.magic_point = 0
        self.magic_point_max = 0
        self.damage_output = [0.5 * strength, 1.5 * strength]
        self.armor_point = 0
        self.level = 1
        self.exp = 0
        self.exp_tot = 0
        self.inventory = inventory.Inventory()
        self.alive = (self.health > 0)
        self.position = position

    def take_damage_from(self, attacker):
        damage = attacker.damage_output[0]
        print("Hit! " + str(int(damage)))
        self.health -= damage
        self.alive = (self.health > 0)

    def aff_equipment(self):
        equipments = self.inventory.slots
        aff = ""
        for i in list(equipments):
            aff += i + " - " + equipments[i] + "\n"
        return aff
