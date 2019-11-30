import platform
import os
import character as ch
import initMap as gen
import item as it
import sqlite3


class Game:

    def __init__(self, bdd, player: ch.Character, list_monster):
        """
        initialize the game Object
        :param bdd:
        :param player:
        :param list_monster:
        """
        cursor = bdd.cursor()
        cursor.execute("SELECT valeur FROM GENERAL WHERE name=\"nb_game\"")
        a = cursor.fetchone()
        cursor.execute("UPDATE GENERAL SET valeur=? WHERE name=\"nb_game\"", (a[0]+1,))
        bdd.commit()
        self.player = player
        self.current_map = gen.Generator()
        self.current_map.gen_level()
        self.current_map.gen_tiles_level()
        self.current_map.init_monster(list_monster)
        self.current_map.init_exit()
        self.player.position = self.current_map.new_map_player()
        self.others_entity = []
        self.level = 1

    def fight(self, opponent1: ch.Character, opponent2: ch.Character, bdd):
        """
        run the fight between 2 characters
        :param opponent1:
        :param opponent2:
        :param bdd:
        :return:
        """
        cursor = bdd.cursor()
        print(opponent1.name + " engages " + opponent2.name)
        block_shield = opponent1.shield_point
        skills = opponent1.spells
        while True:
            print(opponent1.name + ": " + str(opponent1.health) + "\t\t\t\t" + opponent2.name + ": " + str(
                opponent2.health))

            opponent1.attacks(opponent2)
            if not opponent2.alive:
                break

            opponent2.attacks(opponent1)
            if not opponent1.alive:
                break

        if not opponent2.alive:
            print("You win")
            print("Butin:")
            opponent2.show_exp()
            opponent1.level_up(opponent2.exp)
            opponent1.obtain(opponent2.inventory)
            cursor.execute("SELECT valeur FROM GENERAL WHERE name=\"nb_kill\"")
            a = cursor.fetchone()
            cursor.execute("UPDATE GENERAL SET valeur=? WHERE name=\"nb_kill\"", (a[0] + 1,))
            bdd.commit()
            opponent1.shield_point = block_shield
            opponent1.spells = skills
            input()

    def inventory_view(self, someone: ch.Character):
        """
        run the different view of the inventory
        :param someone:
        :return:
        """
        again = True
        print("What do you want to do?")
        print("1) Your inventory")
        print("2) Your equipment")
        print("3) Your statistics")
        print("4) Your success")
        print("5) Your skills")
        print("6) Return")
        view_choice = self.choice(1, 6)
        view_choice = int(view_choice)
        if view_choice == 1:
            items = someone.inventory.show()
            if len(someone.inventory.inventory) == 0:
                input("[PRESS any touch to continue]")
            elif len(someone.inventory.inventory) > 0:
                again_inv = True
                print("What do you want to equip ? (0 : nothing)")
                inv_choice = self.choice(0, len(someone.inventory.inventory))
                inv_choice = int(inv_choice)
                if inv_choice == 0:
                    pass
                else:
                    inv_choice -= 1
                    item = items[inv_choice]
                    if isinstance(item, it.Consumable):
                        print("You can't equip a consumable")
                    elif item.equiped:
                        print("You have already equiped this item")
                    else:
                        item.equiped = True
                        if item.category == "Weapon":
                            print("In which slot do you want to equip it?")
                            print("1) Right Hand, 2) Left Hand")
                            slot_choice = self.choice(1, 2)
                            slot_choice = int(slot_choice)
                            if slot_choice == 1:
                                if isinstance(someone.inventory.slots['right hand'], it.Item):
                                    someone.unequip(someone.inventory.slots['right hand'])
                                    someone.inventory.slots['right hand'].equiped = False
                                someone.inventory.slots['right hand'] = item
                                someone.equip(item)
                            elif slot_choice == 2:
                                if isinstance(someone.inventory.slots['left hand'], it.Item):
                                    someone.unequip(someone.inventory.slots['left hand'])
                                    someone.inventory.slots['left hand'].equiped = False
                                someone.inventory.slots['left hand'] = item
                                someone.equip(item)
                        elif item.category == "Jewels":
                            print("In which slot do you want to equip it?")
                            print("1) Right Hand, 2) Left Hand")
                            slot_choice = self.choice(1, 2)
                            slot_choice = int(slot_choice)
                            if slot_choice == 1:
                                if isinstance(someone.inventory.slots['right jewel'], it.Item):
                                    someone.unequip(someone.inventory.slots['right jewel'])
                                    someone.inventory.slots['right jewel'].equiped = False
                                someone.inventory.slots['right jewel'] = item
                                someone.equip(item)
                            elif slot_choice == 2:
                                if isinstance(someone.inventory.slots['left jewel'], it.Item):
                                    someone.unequip(someone.inventory.slots['left jewel'])
                                    someone.inventory.slots['left jewel'].equiped = False
                                someone.inventory.slots['left jewel'] = item
                                someone.equip(item)
                        else:
                            if isinstance(someone.inventory.slots[item.category], it.Item):
                                someone.unequip(someone.inventory.slots[item.category])
                                someone.inventory.slots[item.category].equiped = False
                            someone.inventory.slots[item.category] = item
                            someone.equip(item)
        elif view_choice == 2:
            slots = ['left hand', 'right hand', 'left jewel', 'right jewel', 'head', 'chest', 'pants', 'arms', 'legs']
            someone.show_slots()
            print("What do you want to unequip ? (0 : nothing)")
            eq_choice = self.choice(0, 9)
            eq_choice = int(eq_choice) - 1
            if eq_choice == 0:
                pass
            else:
                if isinstance(someone.inventory.slots[slots[eq_choice]], it.Item):
                    someone.unequip(someone.inventory.slots[slots[eq_choice]])
                    someone.inventory.slots[slots[eq_choice]].equiped = False
                someone.inventory.slots[slots[eq_choice]] = '-'
        elif view_choice == 3:
            someone.view_stats()
            input()
        elif view_choice == 4:
            someone.view_success()
            input()
        elif view_choice == 5:
            self.change_skills(self.player)
                    
    def trade_display (self, player, merchant):
        """
        run the trade with a merchant
        :param player:
        :param merchant:
        :return:
        """
        test = True
        while test:
            print("Hello brave adventurer do you want to do some business with me ?")
            print("1) Buy")
            print("2) Sell")
            print("0) Leave")

            int_choice = self.choice(0, 2)
            int_choice = int(int_choice)
            if int_choice == 0:
                test = False
                break
            elif int_choice == 1:
                while True:
                    n = 1
                    list_quant = []
                    list_prices = []
                    for i in merchant.inventory.inventory.keys():
                        print(str(n) + ')', i.name, "unit price :", str(i.price), "disp : x" + str(merchant.inventory.inventory[i]))
                        list_quant.append(merchant.inventory.inventory[i])
                        list_prices.append(merchant.inventory.inventory[i])
                        n += 1

                    print("0) Leave")

                    print("Which one do you want to buy ?")
                    int_item = input()
                    if len(int_item) == 1 and 0 <= int(int_item) < n:
                        if int_item == '0':
                            pass
                        else:
                            int_item = int(int_item)
                            print("How many do you want ?")
                            int_quant = input()
                            if len(int_quant) == 1 and 0 < int(int_quant) <= list_quant[int(int_item)-1]:
                                int_quant = int(int_quant)
                                if player.inventory.gold >= list_prices[n-2] * int_choice:
                                    i = list(merchant.inventory.inventory.keys())[int_item-1]
                                    if i in player.inventory.inventory:
                                        player.inventory.inventory[i] += int_quant
                                    else:
                                        player.inventory.inventory[i] = int_quant
                                    merchant.inventory.inventory[i] -= int_quant
                                    player.inventory.gold -= list_prices[n-2] * int_choice
                                break
                            break
            elif int_choice == 2:

                n = 1
                list_quant = []
                list_prices = []
                for i in player.inventory.inventory.keys():
                    print(str(n)  + ')' , i.name , "unit price :", str(i.price), "disp : x" + str(player.inventory.inventory[i]))
                    list_quant.append(player.inventory.inventory[i])
                    list_prices.append(player.inventory.inventory[i])
                    n += 1

                print("0) Leave")

                print("Which one do you want to sell ?")
                int_item = input()
                if len(int_item) == 1 and 0 <= int(int_item) < n:
                    if int_item == '0':
                        pass
                    else:
                        print("How many do you want sell ?")
                        int_quant = input()
                        if len(int_quant) == 1 and 0 < int(int_quant) <= list_quant[int(int_item)-1]:
                            if player.inventory.gold >= list_prices[n-2] * int_choice:
                                i = list(player.inventory.inventory.keys())[int(int_item)-1]
                                player.inventory.inventory[i] -= int(int_quant)
                                player.inventory.gold += list_prices[n-2] * int(int_quant)
                            break
                        break
            break

    def change_skills(self, player):
        """
        manage the skills
        :param player:
        :return:
        """
        test = True
        while test:
            print("Your current skills in use :")
            n = 1
            name_list_spell = []
            for i in player.spells.keys():
                if player.spells[i] is None:
                    pass
                else:
                    name_spell = player.spells[i][0]
                    stat_spell = player.spells[i][1]
                    print(str(i) + ")", name_spell, "cost:", str(stat_spell[3]), "cd :",
                          str(stat_spell[1]))
                    name_list_spell.append(name_spell)
                    n += 1

            for i in range(n, 5):
                print(str(i) + ")")
            print("What would you want to do ?")
            print("1) Change your skill 1)")
            print("2) Change your skill 2)")
            print("3) Change your skill 3)")
            print("4) Change your skill 4)")
            print("0) Leave")
            int_choice = self.choice(0, 4)
            if int(int_choice) == 0:
                test = False

            else:
                n = 1

                for j in player.book.keys():
                    if j in name_list_spell:
                        print(str(n) + ")", j, "cost:", str(player.book[j][3]), "cd :", str(player.book[j][1]), "(eq)")

                    else:
                        print(str(n) + ")", j, "cost:", str(player.book[j][3]), "cd :", str(player.book[j][1]))
                    n += 1

                print("Which spell do you want to use now ?")

                i = list(player.book.keys())
                int_spell = self.choice(1, len(i))
                if len(int_choice) == 1 and 0 < int(int_choice) <= len(i):
                    print(player.book[i[int(int_spell)-1]])
                    player.spells[int(int_choice)] = [i[int(int_spell)-1], player.book[i[int(int_spell)-1]]]
            self.clear_screen()

    @staticmethod
    def clear_screen():
        """
        Clears the terminal screen.
        """

        # Clear command as function of OS
        command = "cls" if platform.system().lower() == "windows" else "clear"
        os.system(command)
        # Action
        return  # subprocess.call(command) == 0

    @staticmethod
    def choice(start: int, end: int):
        """
        function to choose a specific number
        :param start:
        :param end:
        :return:
        """
        again = True
        while again:
            c = input()
            try:
                if start <= int(c) <= end:
                    again = False
            except ValueError:
                pass
        return c

    def new_level(self, list_monster):
        """
        generate the new level
        :param list_monster:
        :return:
        """
        self.current_map = gen.Generator()
        self.current_map.gen_level()
        self.current_map.gen_tiles_level()
        self.current_map.init_monster(list_monster)
        self.current_map.init_exit()
        self.player.position = self.current_map.new_map_player()
