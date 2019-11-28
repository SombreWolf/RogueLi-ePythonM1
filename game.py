import character as ch
import initMap as gen

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
            print(opponent1.name + ": " + opponent1.health + "\t\t\t\t" + opponent2.name + ": " + opponent2.health)
            opponent1.fight()
            if not opponent2.alive:
                break
            opponent2.fight()
            if not opponent1.alive:
                break
        if not opponent2.alive:
            # golds +> item
            print("You win, and you have " + opponent1)
            print("Butin:")
            opponent2.show_exp()
            opponent1.level_up(opponent2.exp)
            opponent2.show_loot()
            opponent1.obtain(opponent2.inventory)
            input()

    def inventory_view(self, someone):
        print("What do you want to do?")
        print("1) Your inventory")
        print("2) Your equipment")
        print("3) Your statistics")
        print("4) Your success")
        while True:
            view_choice = input()
            if len(view_choice) == 1 and 0 < int(view_choice) < 5:
                break
        if view_choice == 1:
            someone.inventory.show()
            if len(someone.inventory.inventory) == 0:
                input("[PRESS any touch to continue]")
            elif len(someone.inventory.inventory) > 0:
                print("What do you want to equip ? (0 : nothing")
                while True:
                    
