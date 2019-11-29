import item as it
import inventory as inv
import random

categoryL = ["Player", "Monster", "Merchant"]


class Character:

    def __init__(self, name="Mob", category="None", health=10, strength=5, position=[0, 0], inventory=inv.Inventory(),
                 exp=10):
        """

        :param name:
        :param category:
        :param health:
        :param strength:
        :param position:
        :param inventory:
        :param exp:
        """
                 exp=10, shield=0, dodge=0, parry=0, critic=random.randint(0, 5), magic_point=0, armor=1, level=1,
                 book={"Basic attack": [1, 0, 0, 0], "Punch": [2, 1, 0, 0]},
                 spells={1: ["Basic attack", [1, 0, 0, 0]], 2: None, 3: None, 4: None}):
        self.name = name
        self.category = category
        self.strength = strength
        self.health = health
        self.health_max = health
        self.shield_point = shield
        self.dodge_chance = dodge
        self.parry_chance = parry
        self.critic_chance = critic
        self.magic_point = magic_point
        self.magic_point_max = magic_point
        self.armor_point = armor
        self.level = level
        self.exp = exp
        self.exp_tot = 0
        self.inventory = inventory
        self.alive = (self.health > 0)
        self.position = position
        self.book = book
        self.spells = spells

    def attacks(self, target):
        """
        function to deal damage no matter the skill you choose to hit
        :param target:
        :return:
        """
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
                spell = self.choice(1, 4)

            elif self.category == "Monster":
                while True:
                    spell = random.randint(1, len(self.spells))
                    if self.spells[spell] is not None:
                        break

            spell = int(spell)

            if self.spells[spell][1][3] < self.magic_point or self.spells[spell][1][2] != 0:
                print(self.name + " uses half assed attack")
                target.defence(self.strength // 2)
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
                    target.defence(self.spells[spell][1][0] * self.strength * 2)
                    return

                else:
                    print(self.name + " uses " + self.spells[spell][0])
                    target.defence(self.spells[spell][1][0] * self.strength)
                    return

    def defence(self, damage):
        """
        function to calculate the reduction damage of an incoming attack
        :param damage:
        :return:
        """
        damage *= 100/(100+self.armor_point)
        dodge = [True for i in range(0, self.dodge_chance)] + [False for i in range(0, 100-self.dodge_chance)]
        parry = [True for i in range(0, self.parry_chance)] + [False for i in range(0, 100-self.parry_chance)]
        if dodge[random.randint(0, 99)]:
            print(self.name + " dodges the attack")

        elif parry[random.randint(0, 99)]:
            print(self.name + " parries the attack and suffer " + str(30*damage//100))#si pb *32 //128 rester en binaire
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
        """
        function to modify your equipment
        :return:
        """
        equipments = self.inventory.slots
        aff = ""
        for i in list(equipments):
            aff += i + " - " + equipments[i] + "\n"

        return aff

    def show_exp(self):
        """
        function to display the exp (mostly used case : after combat)
        :return:
        """
        print(str(self.exp) + " exp")

    def level_up(self, exp):
        """
        function to display all stats and others when you level up
        :param exp:
        :return:
        """
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
            gap = 3 ** self.level
            up = True

        if up:
            print("You level up!")
            print("Your level is now " + str(self.level))

    def obtain(self, inventory):
        """
        function to determine if the player loots some items or not and display the gold and
        :param inventory:
        :return:
        """
        for i in list(inventory.inventory.keys()):
            if random.randint(1, 10) == 10:
                if i in self.inventory.inventory:
                    self.inventory.inventory[i] += inventory.inventory[i]

                else:
                    self.inventory.inventory[i] = inventory.inventory[i]
                print(i.name + " (x" + str(inventory[i]) + ")")

        self.inventory.gold += inventory.gold
        print("Golds : " + str(inventory.gold))

    def show_slots(self):
        """
        function to show your equipment
        :return:
        """
        slots = ['left hand', 'right hand', 'left jewel', 'right jewel', 'head', 'chest', 'pants', 'arms', 'legs']
        for i in list(self.inventory.slots.keys()):
            if isinstance(self.inventory.slots[i], str):
                print(str(slots.index(i) + 1) + ") " + i + " : - ")

            else:
                print(str(slots.index(i)+1) + ") " + i + " : " + self.inventory.slots[i].name)

    def view_stats(self):
        """
        function to display
        :return:
        """
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
        """
        function to display the success on the screen
        :return:
        """
        for i in list(self.inventory.success.keys()):
            string = i + ": "
            if self.inventory.success[i][0]:
                string += self.inventory.success[i][1]

            else:
                string += "Hidden"

            print(string)
        print()

    def equip(self, item: it.Equipment):
        """
        function to equip an pice of equipment
        :param item:
        :return:
        """
        self.health_max += item.special_stats[0]
        self.magic_point_max += item.special_stats[1]
        self.strength += item.power[0]
        self.armor_point += item.power[1]
        self.shield_point += item.special_trait[1]
        self.critic_chance += item.special_trait[0]
        self.dodge_chance += item.dodge_chance
        self.parry_chance += item.parry_chance

    def unequip(self, item: it.Equipment):
        """
        function to unequip a piece of equipment
        :param item:
        :return:
        """
        self.health_max -= item.special_stats[0]
        self.magic_point_max -= item.special_stats[1]
        self.strength -= item.power[0]
        self.armor_point -= item.power[1]
        self.shield_point -= item.special_trait[1]
        self.critic_chance -= item.special_trait[0]
        self.dodge_chance -= item.dodge_chance
        self.parry_chance -= item.parry_chance

    def choice(self, start: int, end: int):
        again = True
        while again:
            c = input()
            try:
                if start <= int(c) <= end:
                    again = False
            except ValueError:
                pass
        return c
