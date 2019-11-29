import item as it
import inventory as inv
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

    def __init__(self, name="Mob", category="None", health=10, strength=5, position=[0, 0], inventory=inv.Inventory(), exp=10):
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
        self.exp = exp
        self.exp_tot = 0
        self.inventory = inventory
        self.alive = (self.health > 0)
        self.position = position
        self.book = {"Basic attack": [1, 0, 0, 0], "Punch": [2, 1, 0, 0]}
        self.spells = {1: ["Basic attack", [1, 0, 0, 0]], 2: None, 3: None, 4: None}

    def attacks(self, target):
        while target.alive:
            if self.category == "Player":
                print("You have :" + str(self.magic_point) + " MP")
                print("What skill do you want to use?")
                print(self.spells)
                for i in range(1, 5):
                    if self.spells[i] is None:
                        pass
                    else:
                        s = str(i) + ") " + self.spells[i][0]
                        if self.spells[i][1][3] != 0:
                            s += " Cost: " + str(self.spells[i][1][3]) + " MP"
                        if self.spells[i][1][1] != 0:
                            s += " CD: " + str(self.spells[i][1][2]) + '/' + str(self.spells[i][1][1])
                        print(s)
                while True:
                    spell = input()
                    if len(spell) == 1 and 0 < int(spell) < len(self.spells)-1:
                        break
                    print("Please choose a correct choice")
            elif self.category == "Monster":
                while True:
                    spell = random.randint(1, len(self.spells))
                    if self.spells[spell] is not None:
                        break

            spell = int(spell)

            if self.spells[spell][1][3] < self.magic_point or self.spells[spell][1][2] != 0:
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

                    if self.spells[i] is not None and self.spells[i][1][1] != self.spells[i][1][2]:
                        self.spells[i][1][2] -= 1
                self.spells[spell][1][2] = self.spells[spell][1][1]
                critic = [True for i in range(0, self.critic_chance)] + [False for i in range(0, 100-self.critic_chance)]
                is_critic = critic[random.randint(0, 99)]
                if is_critic:
                    print(self.name + " uses " + self.spells[spell][0] + " critic!")
                    target.defence(self.spells[spell][1][0] * self.damage_output[2])
                    return
                else:
                    print(self.name + " uses " + self.spells[spell][0])
                    target.defence(self.spells[spell][1][0] * self.damage_output[1])
                    return

    def defence(self, damage):
        damage *= 100/(100+self.armor_point)
        dodge = [True for i in range(0, self.dodge_chance)] + [False for i in range(0, 100-self.dodge_chance)]
        parry = [True for i in range(0, self.parry_chance)] + [False for i in range(0, 100-self.parry_chance)]
        if dodge[random.randint(0, 99)]:
            print(self.name + " dodges the attack")
        elif parry[random.randint(0, 99)]:
            print(self.name + " parries the attack and suffer " + str(30*damage//100)) #si pb *32 //128 rester en binaire
            if self.shield_point - (30*damage//100) < 0:
                  self.health += self.shield_point - (30*damage//100)
                  self.shield_point = 0
            else:
                  self.shield_point -= (30*damage//100)
            
            self.alive = (self.health > 0)
        else:
            print(self.name + " suffer " + str(damage))
            self.health -= int(damage)
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
        gap = 3 ** self.level
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
            gap = 3 ** self.level
            up = True
        if up:
            print("You level up!")
            print("Your level is now " + str(self.level))

    def show_loot(self):
        inventory = self.inventory.inventory
        for i in list(inventory.keys()):
            print(i.name + " (x" + str(inventory[i]) + ")")
        print("Golds : " + str(self.inventory.gold))

    def obtain(self, inventory):
        for i in list(inventory.inventory.keys()):
            if i in self.inventory.inventory:
                self.inventory.inventory[i] += inventory.inventory[i]
            else:
                self.inventory.inventory[i] = inventory.inventory[i]
        self.inventory.gold += inventory.gold

    def show_slots(self):
        slots = ['left hand', 'right hand', 'left jewel', 'right jewel', 'head', 'chest', 'pants', 'arms', 'legs']
        for i in list(self.inventory.slots.keys()):
            if isinstance(self.inventory.slots[i], str):
                print(str(slots.index(i) + 1) + ") " + i + " : - ")
            else:
                print(str(slots.index(i)+1) + ") " + i + " : " + self.inventory.slots[i].name)

    def view_stats(self):
        print("Your Statistics:")
        print("HP: " + str(self.health) + "/" + str(self.health_max))
        print("MP: " + str(self.magic_point) + "/" + str(self.magic_point_max))
        print("Exp: " + str(self.exp) + "/" + str(3 ** self.level))
        print("Strenght: " + str(self.strength))
        print("Armor: " + str(self.armor_point))
        print("Shield: " + str(self.shield_point))
        print("Chance of dodge: " + str(self.dodge_chance))
        print("Chance of parry: " + str(self.parry_chance))
        print("Chance of critical hit: " + str(self.critic_chance))
        input()

    def view_success(self):
        for i in list(self.inventory.success.keys()):
            string = i + ": "
            if self.inventory.success[i][0]:
                string += self.inventory.success[i][1]
            else:
                string += "Hidden"
            print(string)
        print()

    def equip(self, item: it.Equipment):
        self.health_max += item.special_stats[0]
        self.magic_point_max += item.special_stats[1]
        self.strength += item.power[0]
        self.armor_point += item.power[1]
        self.shield_point += item.special_trait[1]
        self.critic_chance += item.special_trait[0]
        self.dodge_chance += item.dodge_chance
        self.parry_chance += item.parry_chance

    def unequip(self, item: it.Equipment):
        self.health_max -= item.special_stats[0]
        self.magic_point_max -= item.special_stats[1]
        self.strength -= item.power[0]
        self.armor_point -= item.power[1]
        self.shield_point -= item.special_trait[1]
        self.critic_chance -= item.special_trait[0]
        self.dodge_chance -= item.dodge_chance
        self.parry_chance -= item.parry_chance
