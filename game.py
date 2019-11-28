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
