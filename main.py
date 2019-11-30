import random
import copy
import game as g
import character as char
import inventory as inv
import item as it
import sqlite3 as sql
import pickle as pic


def menu(bdd):
    """
        function which will "do the game"
    """
    print("EtheralLoop")
    try:
        game = pic.load(open('save\\saves.save', 'rb'))
    except FileNotFoundError:
        print("What is your name adventurer?")
        name = input()
        player = char.Character(name, "Player", exp=0, strenght=10, dodge=random.randint(1, 5),
                                parry=random.randint(1, 5),
                                critic=random.randint(1, 5), magic_point=10)
        list_monster = pic.load(open('Save\\init\\Floor_1_mod4.monst', 'rb'))
        dict_monster_1 = pic.load(open('Save\\init\\List_1_mod4.monst', 'rb'))
        merchant = pic.load(open('Save\\init\\Merchant_floor_1_mod4.monst', 'rb'))
        game = g.Game(bdd, player, list_monster)
        game.current_map.init_monster(['$'])
        dict_monster = {}
        for i in dict_monster_1:
            dict_monster[i.name.upper()[0]] = i
    again = True
    while again:
        game.current_map.display_map_player()
        print("(I)nventory, (L)eave")
        print("(Q)Left,(S)Down,(D)Right,(Z)Up")
        while True:
            choice = input().upper()
            if choice in ['Z', 'Q', 'S', 'D', 'I', 'L']:
                break
        if choice == 'I':
            game.inventory_view(game.player)
        elif choice == 'L':
            pic.dump(game, open('save\\saves.save', 'wb'))
            again = False
        else:
            pos = game.player.position
            if choice == 'S':
                pos2 = [0, 1]
            elif choice == 'Q':
                pos2 = [-1, 0]
            elif choice == 'Z':
                pos2 = [0, -1]
            else:
                pos2 = [1, 0]
            if game.current_map.tiles_level[pos[1] + pos2[1]][pos[0] + pos2[0]] == '$':
                game.trade_display(game.player, merchant)
            elif game.current_map.tiles_level[pos[1] + pos2[1]][pos[0] + pos2[0]] == '#':
                pass
            elif game.current_map.tiles_level[pos[1] + pos2[1]][pos[0] + pos2[0]] in list(dict_monster.keys()):
                monster = dict_monster[game.current_map.tiles_level[pos[1] + pos2[1]][pos[0] + pos2[0]]]
                game.fight(game.player, copy.deepcopy(monster), bdd)
                if game.player.alive:
                    tmp = list(game.current_map.tiles_level[pos[1] + pos2[1]])
                    tmp[pos[0] + pos2[0]] = '.'
                    game.current_map.tiles_level[pos[1] + pos2[1]] = ''.join(tmp)
                    game.current_map.move_to_player(pos, pos2)
                    game.player.position = [pos[0] + pos2[0], pos[1] + pos2[1]]
                if not game.player.alive:
                    again = False
            elif game.current_map.tiles_level[pos[1] + pos2[1]][pos[0] + pos2[0]] == '▓':
                game.level += 1
                game.new_level(
                    pic.load(open('Save\\init\\Floor_' + str(game.level % 4) + '_mod4.monst', 'rb')))
                dict_monster_1 = pic.load(
                    open('Save\\init\\List_' + str(game.level % 4) + '_mod4.monst', 'rb'))
                dict_monster = {}
                for i in dict_monster_1:
                    dict_monster[i.name.upper()[0]] = i
                list_merchant = pic.load(open('Save\\init\\Merchant_floor_' + str(game.level % 4) + '_mod4.monst', 'rb'))
                game.current_map.init_monster(['$'])

            else:
                game.current_map.move_to_player(pos, pos2)
                game.player.position = [pos[0] + pos2[0], pos[1] + pos2[1]]


if __name__ == '__main__':
    bdd = sql.connect('EtheralLoop.db')
    menu(bdd)
    bdd.commit()
    bdd.close()
