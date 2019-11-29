import platform
import subprocess

import character as ch
import initMap as gen
import item as it

# TODO BDD general stats


class Game:
    number_of_game_played = 0
    number_of_monsters_killed = 0
    number_of_fight_with_weapon = {}

    def __init__(self):
        self.player = ch.Character()
        self.current_map = gen.Generator()
        self.others_entity = []

    @staticmethod
    def fight(opponent1: ch.Character, opponent2: ch.Character):

        print(opponent1.name + " engages " + opponent2.name)
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
            # golds +> item
            print("You win")
            print("Butin:")
            opponent2.show_exp()
            opponent1.level_up(opponent2.exp)
            opponent2.show_loot()
            opponent1.obtain(opponent2.inventory)
            input()

    def inventory_view(self, someone):
        again = True
        print("What do you want to do?")
        print("1) Your inventory")
        print("2) Your equipment")
        print("3) Your statistics")
        print("4) Your success")
        print("5) Return")
        while again:
            view_choice = input()
            if len(view_choice) == 1 and 0 < int(view_choice) < 6:
                break
        if view_choice == 1:
            items = someone.inventory.show()
            if len(someone.inventory.inventory) == 0:
                input("[PRESS any touch to continue]")
            elif len(someone.inventory.inventory) > 0:
                print("What do you want to equip ? (0 : nothing")
                while True:
                    inv_choice = input()
                    try:
                        if -1 < int(inv_choice) < len(someone.inventory.inventory):
                            break
                    except ValueError:
                        pass
                if inv_choice == 0:
                    pass
                else:
                    inv_choice -= 1
                    item = items[inv_choice]
                    if isinstance(item, it.Consumable):
                        print("You can't equip a consumable")
                    else:
                        if item.category == "Weapon":
                            print("In which slot do you want to equip it?")
                            print("1) Right Hand, 2) Left Hand")
                            while True:
                                slot_choice = input()
                                if len(slot_choice) == 1 and 0 < int(slot_choice) < 3:
                                    break
                            if slot_choice == 1:
                                someone.inventory.slots['right hand'] = item
                            elif slot_choice == 2:
                                someone.inventory.slots['left hand'] = item
                        elif item.category == "Jewels":
                            print("In which slot do you want to equip it?")
                            print("1) Right Hand, 2) Left Hand")
                            while True:
                                slot_choice = input()
                                if len(slot_choice) == 1 and 0 < int(slot_choice) < 3:
                                    break
                            if slot_choice == 1:
                                someone.inventory.slots['right jewel'] = item
                            elif slot_choice == 2:
                                someone.inventory.slots['left jewel'] = item
                        else:
                            someone.inventory.slots[item.category] = item
        elif view_choice == 2:
            slots = ['left hand', 'right hand', 'left jewel', 'right jewel', 'head', 'chest', 'pants', 'arms', 'legs']
            someone.show_slots()
            print("What do you want to unequip ? (0 : nothing")
            while True:
                eq_choice = input()
                try:
                    if -1 < int(eq_choice) < 10:
                        break
                except ValueError:
                    pass
            if eq_choice == 0:
                pass
            else:
                someone.inventory.slots[slots[eq_choice]] = '-'
        elif view_choice == 3:
            someone.view_stats()
        elif view_choice == 4:
            someone.view_success()
                    
    def trade_display (player, merchant):
        test = True
        while test:
            print("Hello brave adventurer do you want to do some business with me ?")
            print("1) Buy")
            print("2) Sell")
            print("0) Leave")
            
            while True:
                int_choice = input()
                if len(int_choice) == 1 and 0 <= int(int_choice) < 3:
                    if int_choice == 0:
                        test = False
                        break
                    elif int_choice == 1:
                        while True:
                            n = 1
                            list_quant = []
                            list_prices = []
                            for i in merchant.inventory.inventory.keys():
                                print(n  + ')', i.name, "unit price :", i.price, "disp : x" +
                                      merchant.inventory.inventory[i])
                                list_quant.append(merchant.inventory.inventory[i])
                                list_prices.append(merchant.inventory.inventory[i])
                                n += 1

                            print("0) Leave")

                            print("Which one do you want to buy ?")
                            int_item = input()
                            if len(int_item) == 1 and 0 <= int(int_item) < n:
                                print("How many do you want ?")
                                int_quant = input()
                                if len(int_quant) == 1 and 0 < int(int_quant) < list_quant[int_quant-1]:
                                    if player.inventory.gold >= list_prices[n] * int_choice:
                                        i = list(merchant.inventory.keys())[int_item]
                                        if i in player.inventory.inventory:
                                            player.inventory.inventory[i] += int_quant
                                        else:
                                            player.inventory.inventory[i] = int_quant
                                        merchant.inventory.inventory[i] -= int_quant
                                        player.inventory.gold -= list_prices[n] * int_choice
                                    break
                                break
                            
                    elif int_choice == 2:

                        n = 1
                        list_quant = []
                        list_prices = []
                        for i in player.inventory.inventory.keys():
                            print(n  + ')' , i.name , "unit price :", i.price, "disp : x" +
                                  player.inventory.inventory[i])
                            list_quant.append(player.inventory.inventory[i])
                            list_prices.append(player.inventory.inventory[i])
                            n += 1

                        print("0) Leave")

                        print("Which one do you want to sell ?")
                        int_item = input()
                        if len(int_choice) == 1 and 0 <= int(int_item) < n:
                            print("How many do you want sell ?")
                            int_quant = input()
                            if len(int_choice) == 1 and 0 < int(int_quant) < list_quant[int_item]:
                                if player.inventory.gold >= list_prices[n] * int_choice:
                                    i = list(player.inventory.keys())[int_item]
                                    player.inventory.inventory[i] -= int_quant
                                    player.inventory.gold += list_prices[n] * int_choice
                                break
                            break
                    break
                
    def change_skills(self, player):

        while test:
            test = True
            print("Your current skills in use :")
            n = 1
            name_list_spell = []
            for i in player.spells.keys():
                name_spell = player.spells[i][0]
                stat_spell = player.spells[i][1]
                print(str(i) + ")", name_spell, "cost:", stat_spell[3], "cd :",
                      stat_spell[1])
                name_list_spell.append(name_spell)
                n += 1

            for i in range(n - 1, 5):
                print(i + ")")
            print("What would you want to do ?")
            print("1) Change your skill 1)")
            print("2) Change your skill 2)")
            print("3) Change your skill 3)")
            print("4) Change your skill 4)")
            print("0) Leave")
            int_choice = input()

            if len(int_choice) == 1 and 0 <= int(int_choice) < 5:
                if int_choice == 0:
                    test = False

                else:
                    n = 1

                    for j in player.book.keys():
                        if j in name_list_spell:
                            print(n + ")", j, "cost:", player.book[j][3], "cd :", player.book[j][1],"(eq)")

                        else:
                            print(n + ")", j, "cost:", player.book[j][3], "cd :", player.book[j][1])
                        n += 1

                    print("Which spell do you want to use now ?")
                    int_spell = input()
                    i = list(player.book.keys())
                    if len(int_choice) == 1 and 0 <= int(int_choice) < len(i):
                        player.spells[int_choice] = player.book[i[int_spell]]
                        break
            self.clear_screen()

    def clear_screen(self):
        """
        Clears the terminal screen.
        """

        # Clear command as function of OS
        command = "cls" if platform.system().lower() == "windows" else "clear"

        # Action
        return subprocess.call(command) == 0