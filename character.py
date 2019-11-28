import inventory
import random

pieces = ['head',
          'hands',
          'left hand',
          'right hand',
          'upper body',
          'legs',
          'feet']

categoryL = ["Player", "Monster", "Merchant"]


class Character:

    def __init__(self, name="Mob", category = "None", health=10, strength=5, position=[0, 0]):
        self.name = name
        self.category = category
        self.strength = strength
        self.health = health
        self.health_max = health
        self.shield_point = 0
        self.dodge_chance = 0
        self.parry_chance = 0
        self.critic_chance = random.randint(0, 5)
        self.magic_point = 0
        self.magic_point_max = 0
        self.damage_output = [strength//2, strength, 2 * strength]
        self.armor_point = 0
        self.level = 1
        self.exp = 0
        self.exp_tot = 0
        self.inventory = inventory.Inventory()
        self.alive = (self.health > 0)
        self.position = position
        self.book = {"Basic attack": [1, 1, 0, 0]}
        self.spells = {1: ["Basic attack", [1, 1, 1, 0]]}

    def attacks(self, target):
        while target.alive:
            if self.category == "Player":
                print("You have :" + str(self.magic_point) + " MP")
                print("What skill do you want to use?")
                for i in range(1, len(self.spells)+1):
                    s = str(i)+") "
                    if self.spells[i][1][3] != 0:
                        s += "Cost: " + str(self.spells[i][1][3]) + " MP"
                    if self.spells[i][1][1] != 0:
                        s += "CD: " + str(self.spells[i][1][2])
                    print(s)
                while True:
                    spell = input()
                    if len(spell) == 1 and 0 < int(spell) < len(self.spells)+1:
                        break
                    print("Please choose a correct choice")
            elif self.category == "Monster":
                spell = random.randint(1, len(self.spells))

            if self.spells[spell][1][3] < self.magic_point or self.spells[i][1][2] != 0:
                print(self.name + " uses half assed attack")
                target.defence(self.damage_output[0])
                return
            if self.spells[spell][1][3] != 0:
                self.magic_point -= self.spells[spell][1][3]
                print(self.name + " uses " + self.spells[spell][0])
                target.defence(self.spells[spell][1][0]*self.damage_output[1])
                self.attacks(target)
            if self.spells[spell][1][3] == 0:
                for i in self.spells:
                    if i[1][1] != i[1][2]:
                        i[1][2] -= 1
                self.spells[spell][1][2] = self.spells[spell][1][1]
                critic = [True for i in range(0, self.critic_chance)] + [False for i in range(0, 100-self.critic_chance)]
                is_critic = critic[random.randint(0, 99)]
                if is_critic:
                    print(self.name + " uses " + self.spells[spell][0] + " critic!")
                    target.defence(self.spells[spell][1][0] * self.damage_output[2])
                else:
                    print(self.name + " uses " + self.spells[spell][0])
                    target.defence(self.spells[spell][1][0] * self.damage_output[1])

    def defence(self, damage):
        damage *= 100/(100+self.armor_point)
        dodge = [True for i in range(0, self.dodge_chance)] + [False for i in range(0, 100-self.dodge_chance)]
        parry = [True for i in range(0, self.parry_chance)] + [False for i in range(0, 100-self.parry_chance)]
        if dodge[random.randint(0, 99)]:
            print(self.name + " dodges the attack")
        elif parry[random.randint(0, 99)]:
            print(self.name + " parries the attack and suffer " + str(int(0.7*damage)))
            self.health -= damage
            self.alive = (self.health > 0)
        else:
            print(self.name + " suffer " + str(damage))
            self.health -= int(0.7 * damage)
            self.alive = (self.health > 0)

    def aff_equipment(self):
        equipments = self.inventory.slots
        aff = ""
        for i in list(equipments):
            aff += i + " - " + equipments[i] + "\n"
        return aff

    def show_exp(self):
        print(str(self.exp) + " exp")

    def level_up(self, exp):
        up = False
        self.exp += exp
        self.exp_tot += exp
        gap = 3**self.level
        while self.exp >= gap:
            self.exp -= gap
            self.level += 1
            self.health_max += 10
            self.health = self.health_max
            self.magic_point_max += 5
            self.magic_point += 5
            self.armor_point += 3
            self.strength += 3
            self.damage_output = [self.strength // 2, self.strength, 2 * self.strength]
            up = True
        if up:
            print("You level up!")
            print("Your level is now " + str(self.level))

    def show_loot(self):
        inv = self.inventory.inventory
        for i in inv.keys():
            print(i.name + "(" + inv[i] + "x)")
        print("Golds : " + self.inventory.gold)

    def obtain(self, inv):
        for i in inv.keys():
            if i in self.inventory.inventory:
                self.inventory.inventory[i] += inv.inventory[i]
            else:
                self.inventory.inventory[i] = inv.inventory[i]
        self.inventory.gold += inv.gold
